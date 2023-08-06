import random
import time

import numpy as np
import pytorch_lightning as pl
import torch
from litsr.archs import create_net
from litsr.data.degradations import (
    random_add_gaussian_noise_pt,
    random_add_poisson_noise_pt,
)
from litsr.metrics import calc_psnr_ssim
from litsr.transforms import paired_random_crop, tensor2uint8
from litsr.utils import DiffJPEG, USMSharp, filter2D
from litsr.utils.registry import ModelRegistry
from torch.nn import functional as F


@ModelRegistry.register()
class RealESRNetModel(pl.LightningModule):
    """
    SR Model for real esrgan
    """

    def __init__(self, opt):
        """
        opt: in_channels, out_channels, num_features, num_blocks, num_layers
        """
        super().__init__()

        # save hyperparameters
        self.save_hyperparameters(opt)

        # init super-resolution network
        self.sr_net = create_net(opt["network"])
        self.usm_sharpener = USMSharp()
        self.jpeger = DiffJPEG(differentiable=False)
        self.queue_size = opt.get("queue_size", 180)

        # define loss function (L1 loss)
        self.loss_fn = torch.nn.L1Loss()

    @torch.no_grad()
    def _dequeue_and_enqueue(self):
        # training pair pool
        # initialize
        b, c, h, w = self.lq.size()
        if not hasattr(self, "queue_lr"):
            assert (
                self.queue_size % b == 0
            ), "queue size should be divisible by batch size"
            self.queue_lr = torch.zeros(self.queue_size, c, h, w).cuda()
            _, c, h, w = self.gt.size()
            self.queue_gt = torch.zeros(self.queue_size, c, h, w).cuda()
            self.queue_ptr = 0
        if self.queue_ptr == self.queue_size:  # full
            # do dequeue and enqueue
            # shuffle
            idx = torch.randperm(self.queue_size)
            self.queue_lr = self.queue_lr[idx]
            self.queue_gt = self.queue_gt[idx]
            # get
            lq_dequeue = self.queue_lr[0:b, :, :, :].clone()
            gt_dequeue = self.queue_gt[0:b, :, :, :].clone()
            # update
            self.queue_lr[0:b, :, :, :] = self.lq.clone()
            self.queue_gt[0:b, :, :, :] = self.gt.clone()

            self.lq = lq_dequeue
            self.gt = gt_dequeue
        else:
            # only do enqueue
            self.queue_lr[
                self.queue_ptr : self.queue_ptr + b, :, :, :
            ] = self.lq.clone()
            self.queue_gt[
                self.queue_ptr : self.queue_ptr + b, :, :, :
            ] = self.gt.clone()
            self.queue_ptr = self.queue_ptr + b

    @torch.no_grad()
    def feed_data(self, data, is_train=True):
        if is_train and self.hparams.get("high_order_degradation", True):
            # training data synthesis
            self.gt = data["gt"]
            # USM the GT images
            if self.hparams.get("gt_usm", True):
                self.gt = self.usm_sharpener(self.gt)

            self.kernel1 = data["kernel1"]
            self.kernel2 = data["kernel2"]
            self.sinc_kernel = data["sinc_kernel"]

            ori_h, ori_w = self.gt.size()[2:4]

            # ----------------------- The first degradation process ----------------------- #
            # blur
            out = filter2D(self.gt, self.kernel1)
            # random resize
            updown_type = random.choices(
                ["up", "down", "keep"], self.hparams["resize_prob"]
            )[0]
            if updown_type == "up":
                scale = np.random.uniform(1, self.hparams["resize_range"][1])
            elif updown_type == "down":
                scale = np.random.uniform(self.hparams["resize_range"][0], 1)
            else:
                scale = 1
            mode = random.choice(["area", "bilinear", "bicubic"])
            out = F.interpolate(out, scale_factor=scale, mode=mode)
            # noise
            gray_noise_prob = self.hparams["gray_noise_prob"]
            if np.random.uniform() < self.hparams["gaussian_noise_prob"]:
                out = random_add_gaussian_noise_pt(
                    out,
                    sigma_range=self.hparams["noise_range"],
                    clip=True,
                    rounds=False,
                    gray_prob=gray_noise_prob,
                )
            else:
                out = random_add_poisson_noise_pt(
                    out,
                    scale_range=self.hparams["poisson_scale_range"],
                    gray_prob=gray_noise_prob,
                    clip=True,
                    rounds=False,
                )
            # JPEG compression
            jpeg_p = out.new_zeros(out.size(0)).uniform_(*self.hparams["jpeg_range"])
            out = torch.clamp(out, 0, 1)
            out = self.jpeger(out, quality=jpeg_p)

            # ----------------------- The second degradation process ----------------------- #
            # blur
            if np.random.uniform() < self.hparams["second_blur_prob"]:
                out = filter2D(out, self.kernel2)
            # random resize
            updown_type = random.choices(
                ["up", "down", "keep"], self.hparams["resize_prob2"]
            )[0]
            if updown_type == "up":
                scale = np.random.uniform(1, self.hparams["resize_range2"][1])
            elif updown_type == "down":
                scale = np.random.uniform(self.hparams["resize_range2"][0], 1)
            else:
                scale = 1
            mode = random.choice(["area", "bilinear", "bicubic"])
            out = F.interpolate(
                out,
                size=(
                    int(ori_h / self.hparams["scale"] * scale),
                    int(ori_w / self.hparams["scale"] * scale),
                ),
                mode=mode,
            )
            # noise
            gray_noise_prob = self.hparams["gray_noise_prob2"]
            if np.random.uniform() < self.hparams["gaussian_noise_prob2"]:
                out = random_add_gaussian_noise_pt(
                    out,
                    sigma_range=self.hparams["noise_range2"],
                    clip=True,
                    rounds=False,
                    gray_prob=gray_noise_prob,
                )
            else:
                out = random_add_poisson_noise_pt(
                    out,
                    scale_range=self.hparams["poisson_scale_range2"],
                    gray_prob=gray_noise_prob,
                    clip=True,
                    rounds=False,
                )

            # JPEG compression + the final sinc filter
            # We also need to resize images to desired sizes. We group [resize back + sinc filter] together
            # as one operation.
            # We consider two orders:
            #   1. [resize back + sinc filter] + JPEG compression
            #   2. JPEG compression + [resize back + sinc filter]
            # Empirically, we find other combinations (sinc + JPEG + Resize) will introduce twisted lines.
            if np.random.uniform() < 0.5:
                # resize back + the final sinc filter
                mode = random.choice(["area", "bilinear", "bicubic"])
                out = F.interpolate(
                    out,
                    size=(
                        ori_h // self.hparams["scale"],
                        ori_w // self.hparams["scale"],
                    ),
                    mode=mode,
                )
                out = filter2D(out, self.sinc_kernel)
                # JPEG compression
                jpeg_p = out.new_zeros(out.size(0)).uniform_(
                    *self.hparams["jpeg_range2"]
                )
                out = torch.clamp(out, 0, 1)
                out = self.jpeger(out, quality=jpeg_p)
            else:
                # JPEG compression
                jpeg_p = out.new_zeros(out.size(0)).uniform_(
                    *self.hparams["jpeg_range2"]
                )
                out = torch.clamp(out, 0, 1)
                out = self.jpeger(out, quality=jpeg_p)
                # resize back + the final sinc filter
                mode = random.choice(["area", "bilinear", "bicubic"])
                out = F.interpolate(
                    out,
                    size=(
                        ori_h // self.hparams["scale"],
                        ori_w // self.hparams["scale"],
                    ),
                    mode=mode,
                )
                out = filter2D(out, self.sinc_kernel)

            # clamp and round
            self.lq = torch.clamp((out * 255.0).round(), 0, 255) / 255.0

            # random crop
            gt_size = self.hparams["gt_size"]
            self.gt, self.lq = paired_random_crop(
                self.lq, self.gt, gt_size, self.hparams["scale"]
            )

            # training pair pool
            self._dequeue_and_enqueue()
        else:
            self.lq = data["lq"].to(self.device)
            if "gt" in data:
                self.gt = data["gt"].to(self.device)
                self.gt_usm = self.usm_sharpener(self.gt)

    def forward(self, lr):
        return self.sr_net(lr)

    def training_step(self, batch, batch_idx):
        self.feed_data(batch)
        sr = self.forward(self.lq)
        loss = self.loss_fn(sr, self.gt)
        return loss

    def training_epoch_end(self, outputs):
        avg_loss = torch.stack([out["loss"] for out in outputs]).mean()
        self.logger.experiment.add_scalar("train_loss", avg_loss, self.global_step)
        return

    def validation_step(self, batch, batch_idx):
        lr, hr, name = batch
        torch.cuda.synchronize()
        start = time.time()
        sr = self.forward(lr).detach()
        torch.cuda.synchronize()
        end = time.time()

        loss = self.loss_fn(sr, hr)
        sr_np, hr_np = tensor2uint8(
            [sr.cpu()[0], hr.cpu()[0]], self.hparams.train.rgb_range
        )

        psnr, ssim = calc_psnr_ssim(
            sr_np, hr_np, crop_border=self.hparams.valid.scale, test_Y=True
        )
        return {
            "val_loss": loss,
            "val_psnr": psnr,
            "val_ssim": ssim,
            "log_img_sr": sr_np,
            "name": name[0],
            "time": end - start,
        }

    def validation_epoch_end(self, outputs):
        tensorboard = self.logger.experiment
        log_img = outputs[0]["log_img_sr"]

        avg_loss = torch.stack([x["val_loss"] for x in outputs]).mean()
        avg_psnr = np.array([x["val_psnr"] for x in outputs]).mean()
        avg_ssim = np.array([x["val_ssim"] for x in outputs]).mean()
        tensorboard.add_scalar("val_loss", avg_loss, self.global_step)
        tensorboard.add_scalar(
            "val_psnr/{0}".format(self.hparams.train.scale), avg_psnr, self.global_step
        )
        tensorboard.add_scalar(
            "val_ssim/{0}".format(self.hparams.train.scale), avg_ssim, self.global_step
        )
        tensorboard.add_image(
            "images/{0}".format(self.hparams.train.scale),
            log_img,
            self.global_step,
            dataformats="HWC",
        )

        self.log("val_psnr", avg_psnr, on_epoch=True, prog_bar=True, logger=False)
        return

    def test_step(self, batch, batch_idx):
        return self.validation_step(batch, batch_idx)

    def configure_optimizers(self):
        betas = self.hparams.train.get("betas") or (0.9, 0.999)
        optimizer = torch.optim.Adam(
            self.parameters(), lr=self.hparams.train.lr, betas=betas
        )
        if self.hparams.train.get("lr_scheduler_step"):
            LR_scheduler = torch.optim.lr_scheduler.StepLR(
                optimizer,
                step_size=self.hparams.train.lr_scheduler_step,
                gamma=self.hparams.train.lr_scheduler_gamma,
            )
        elif self.hparams.train.get("lr_scheduler_milestones"):
            LR_scheduler = torch.optim.lr_scheduler.MultiStepLR(
                optimizer,
                milestones=self.hparams.train.lr_scheduler_milestones,
                gamma=self.hparams.train.lr_scheduler_gamma,
            )
        else:
            raise Exception(
                "No lr settings found in self.hparams.train, please modify the config file"
            )
        return [optimizer], [LR_scheduler]
