import torch
import torch.nn as nn
import numpy as np
import time
from torch.utils.data import DataLoader
from torch.nn import functional as F
from torchvision.utils import make_grid
import pytorch_lightning as pl
from litsr.archs import create_net
from litsr.utils.registry import ModelRegistry

# from models import forward_self_ensemble
# from datasets.ms_dataset import TrainDataset, TestDataset
# from utils.metrics import calc_metrics
# from utils.utils import Tensor2np


# @ModelRegistry.register()
class MultiScaleSRModel(pl.LightningModule):
    def __init__(self, opt):
        """
        hparams: in_channels, out_channels, num_features, num_blocks, num_layers
        """
        super().__init__()

        # save hyperparameters
        self.save_hyperparameters(opt)

        # init super-resolution network
        self.sr_net = create_net(opt["model"])

        # define loss function (L1 loss)
        self.loss_fn = nn.L1Loss()

    def setup(self, mode):
        # setup the train dataset
        if mode == "fit":
            self.train_dataset = TrainDataset(
                self.hparams.train.data_path,
                self.hparams.train.min_scale,
                self.hparams.train.max_scale,
                self.hparams.train.lr_img_sz,
                self.hparams.train.batch_size,
                self.hparams.model.rgb_range,
                self.hparams.train.data_repeat,
                self.hparams.train.data_cache,
                self.hparams.train.data_first_k,
            )
        self.test_dataset = lambda scale: TestDataset(
            self.hparams.test.data_path, scale, self.hparams.model.rgb_range
        )

    def forward(self, lr, out_size):
        return self.sr_net(lr, out_size)

    def forward_self_ensemble(self, lr, out_size):
        return forward_self_ensemble(self, lr, out_size)

    def training_step(self, batch, batch_idx):
        lr, hr = batch
        out_size = hr.shape[2]
        sr = self.forward(lr, out_size)
        loss = self.loss_fn(sr, hr)
        return loss

    def training_epoch_end(self, outputs):
        if "ran" in self.hparams.model.which_network:
            self.sr_net.update_temperature()
        avg_loss = torch.stack([out["loss"] for out in outputs]).mean()
        self.logger.experiment.add_scalar("train_loss", avg_loss, self.global_step)

    def validation_step(self, batch, batch_idx, dataloader_idx):
        lr, hr, name = batch
        out_size = hr.shape[2:]
        torch.cuda.synchronize()
        start = time.time()
        if self.hparams.test.self_ensemble:
            sr = self.forward_self_ensemble(lr, out_size).detach()
        else:
            sr = self.forward(lr, out_size).detach()
        torch.cuda.synchronize()
        end = time.time()
        crop_border = int(np.ceil(float(hr.shape[2]) / lr.shape[2]))
        loss = self.loss_fn(sr, hr).item()

        sr_np, hr_np = Tensor2np(
            [sr.cpu()[0], hr.cpu()[0]], self.hparams.model.rgb_range
        )
        psnr, ssim = calc_metrics(sr_np, hr_np, crop_border=crop_border, test_Y=True)
        return {
            "val_loss": loss,
            "val_psnr": psnr,
            "val_ssim": ssim,
            "log_img": sr_np,
            "name": name[0],
            "time": end - start,
        }

    def validation_epoch_end(self, outputs):
        psnr_list = []
        for idx, dataloader_output_result in enumerate(outputs):
            scale = self.hparams.valid.scales[idx]
            dataloader_outs = dataloader_output_result
            tensorboard = self.logger.experiment

            log_imgs = [x["log_img"] for x in dataloader_outs[12:13]]

            avg_loss = np.array([x["val_loss"] for x in dataloader_outs]).mean()
            avg_psnr = np.array([x["val_psnr"] for x in dataloader_outs]).mean()
            psnr_list.append(avg_psnr)
            tensorboard.add_scalar(
                "val_loss/{0}".format(scale), avg_loss, self.global_step
            )
            tensorboard.add_scalar(
                "val_psnr/{0}".format(scale), avg_psnr, self.global_step
            )
            if log_imgs:
                tensorboard.add_image(
                    "images/{0}".format(scale),
                    log_imgs[0],
                    self.global_step,
                    dataformats="HWC",
                )

        self.log(
            "avg_val_psnr",
            np.array(psnr_list).mean(),
            on_epoch=True,
            prog_bar=True,
            logger=False,
        )

    def configure_optimizers(self):
        if hasattr(self.hparams.train, "betas"):
            betas = self.hparams.train.betas
        else:
            betas = (0.9, 0.999)
        optimizer = torch.optim.Adam(
            self.parameters(), lr=self.hparams.train.lr, betas=betas
        )
        if hasattr(self.hparams.train, "lr_scheduler_step"):
            LR_scheduler = torch.optim.lr_scheduler.StepLR(
                optimizer,
                step_size=self.hparams.train.lr_scheduler_step,
                gamma=self.hparams.train.lr_scheduler_gamma,
            )
        elif hasattr(self.hparams.train, "lr_scheduler_milestones"):
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

    def train_dataloader(self):
        self.train_dataset.resample_scale()
        return DataLoader(
            self.train_dataset,
            batch_size=self.hparams.train.batch_size,
            num_workers=self.hparams.sys.num_workers,
            shuffle=False,
            pin_memory=True,
        )

    def val_dataloader(self):
        dataloaders = []
        for scale in self.hparams.valid.scales:
            dataset = self.test_dataset(scale)
            dataloaders.append(
                DataLoader(
                    dataset,
                    batch_size=1,
                    num_workers=self.hparams.sys.num_workers,
                    pin_memory=True,
                )
            )
        return dataloaders

    def change_params(self, hparams):
        self.hparams = hparams
