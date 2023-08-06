import numpy as np
import torch.utils.data as data
from litsr import transforms
from litsr.data.image_folder import ImageFolder
from litsr.utils.registry import DatasetRegistry
from torchvision import transforms as tv_transforms
from torchvision.transforms import functional as TF


@DatasetRegistry.register()
class DownsampledDataset(data.Dataset):
    def __init__(
        self,
        datapath,
        scale,
        is_train,
        lr_img_sz=None,
        rgb_range=1,
        repeat=1,
        cache=None,
        first_k=None,
        mean=None,
        std=None,
        downsample_mode="bicubic",
        return_img_name=False,
    ):
        assert not is_train ^ bool(lr_img_sz)

        self.scale = scale
        self.lr_img_sz = lr_img_sz
        self.repeat = repeat or 1
        self.rgb_range = rgb_range or 1
        self.is_train = is_train
        self.mean = mean
        self.std = std
        self.return_img_name = return_img_name
        self.downsample_mode = downsample_mode or "bicubic"
        self.dataset = ImageFolder(
            datapath, repeat=self.repeat, cache=cache, first_k=first_k
        )
        self.file_names = self.dataset.filenames

    def __getitem__(self, idx):
        hr = self.dataset[idx]
        if self.is_train:
            lr, hr = self._transform_train(hr)
        else:
            lr, hr = self._transform_test(hr)

        if self.mean and self.std:
            transforms.normalize(lr, self.mean, self.std, inplace=True)
            transforms.normalize(hr, self.mean, self.std, inplace=True)

        if self.return_img_name:
            file_name = self.file_names[idx % (len(self.dataset) // self.repeat)]
            return lr, hr, file_name
        else:
            return lr, hr

    def _transform_train(self, x):
        lr_img_sz = self.lr_img_sz
        hr_img_sz = int(lr_img_sz * self.scale)

        transform = tv_transforms.Compose(
            [
                tv_transforms.ToPILImage(),
                tv_transforms.RandomCrop(hr_img_sz),
                tv_transforms.RandomHorizontalFlip(),
                tv_transforms.RandomVerticalFlip(),
                lambda x: TF.rotate(x, 90) if np.random.random() > 0.5 else x,
                lambda x: [
                    transforms.resize_pillow(
                        x, size=(lr_img_sz, lr_img_sz), mode=self.downsample_mode
                    ),
                    x,
                ],
                lambda x: transforms.pil2tensor(x, self.rgb_range),
            ]
        )
        lr, hr = transform(x)

        return lr, hr

    def _transform_test(self, hr):
        scale = self.scale
        hr = transforms.mod_crop(hr, scale)

        [hr_img_h, hr_img_w] = hr.shape[0:2]
        [lr_img_h, lr_img_w] = [int(hr_img_h // scale), int(hr_img_w // scale)]

        transform = tv_transforms.Compose(
            [
                tv_transforms.ToPILImage(),
                lambda x: [
                    transforms.resize_pillow(
                        x, size=(lr_img_h, lr_img_w), mode=self.downsample_mode
                    ),
                    x,
                ],
                lambda x: transforms.pil2tensor(x, self.rgb_range),
            ]
        )
        lr, hr = transform(hr)

        return lr, hr

    def __len__(self):
        return len(self.dataset)
