# import all data module

from litsr.utils.registry import DataModuleRegistry, DatasetRegistry

from .downsampled_dataset import DownsampledDataset
from .image_folder import ImageFolder, PairedImageFolder
from .paired_image_dataset import PairedImageDataset
from .realesrgan_dataset import RealESRGANDataset
from .realsr_datamodule import RealSRDataModule
from .sr_datamodule import SRDataModule

__all__ = ["create_data_module"]


def create_data_module(opt):
    """ create model from option
    """
    data_module_name = opt.get("data_module")
    if not data_module_name:
        return
    data_module = DataModuleRegistry.get(data_module_name)
    return data_module(opt)
