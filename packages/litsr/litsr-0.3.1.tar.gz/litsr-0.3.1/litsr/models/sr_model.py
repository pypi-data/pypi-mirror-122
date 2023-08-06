import time

import numpy as np
import pytorch_lightning as pl
import torch
import torch.nn as nn
from litsr.archs import create_net
from litsr.transforms import tensor2uint8
from litsr.metrics import calc_psnr_ssim
from litsr.utils.registry import ModelRegistry


@ModelRegistry.register()
class SRModel(pl.LightningModule):
    """
    Basic SR Model optimized by pixel-wise loss
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

        # define loss function (L1 loss)
        self.loss_fn = nn.L1Loss()

    def forward(self, lr):
        return self.sr_net(lr)

    def training_step(self, batch, batch_idx):
        lr, hr = batch
        sr = self.forward(lr)
        loss = self.loss_fn(sr, hr)
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
