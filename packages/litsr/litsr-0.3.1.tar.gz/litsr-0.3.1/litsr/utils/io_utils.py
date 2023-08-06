import json
import os
import re
import shutil
from pathlib import Path
from typing import Iterable, Optional

import cv2
import numpy as np
import yaml
from easydict import EasyDict as Dict
from litsr.transforms import uint2single
from tqdm import tqdm


def read_json(fname):
    """Read json from path
    """
    fname = Path(fname)
    with fname.open("rt") as handle:
        return Dict(json.load(handle))


def write_json(content, fname):
    """Write json to path
    """
    fname = Path(fname)
    with fname.open("wt") as handle:
        json.dump(content, handle, indent=4, sort_keys=False)


def read_yaml(fname):
    """Real yaml from path

    Args:
        fname (str): path

    Returns:
        Easydict: Easydict
    """
    fname = Path(fname)
    with fname.open("rt") as handle:
        return Dict(yaml.load(handle, Loader=yaml.FullLoader))


def mkdir(path):
    """create a single empty directory if it didn't exist

    Parameters:
        path (str) -- a single directory path
    """
    if not os.path.exists(path):
        os.makedirs(path)


def mkdirs(paths):
    """create empty directories if they don't exist

    Parameters:
        paths (str list) -- a list of directory paths
    """
    if isinstance(paths, list) and not isinstance(paths, str):
        for path in paths:
            mkdir(path)
    else:
        mkdir(paths)


def mkdir_clean(path):
    """Create a directory that is guaranteed to be empty 
    """
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            os.makedirs(path)
        except:
            print("warning! Cannot remove {0}".format(path))
    else:
        os.makedirs(path)


def load_file_list(path: str, regx: str) -> list:
    file_list = os.listdir(path)
    return_list = []
    for _, f in enumerate(file_list):
        if re.search(regx, f):
            return_list.append(os.path.join(path, f))
    return sorted(return_list)


def read_image(
    path: str, mode: Optional[str] = "RGB", to_float: bool = False
) -> np.ndarray:
    """Read image to a 3 dimentional numpy by OpenCV
    """
    img = cv2.imread(path)
    assert mode in ("RGB", "BGR")
    if mode == "RGB":
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if to_float:
        img = uint2single(img)
    return img


def read_images(
    path_list: Iterable[str], mode: Optional[str] = "RGB", to_float: bool = False
) -> np.ndarray:
    """Read images to a 4 dimentional numpy array by OpenCV
    """
    rslt = []
    for path in tqdm(path_list):
        rslt.append(read_image(path, mode, to_float))
    return np.array(rslt)
