# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-11 17:55:59
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-18 17:22:36

import os
from datasets import load_dataset

from src.utils import get_module_root
from src.datasets.maptask.maptask import MapTask

DATASET_LOADING_SCRIPT = os.path.join(
    get_module_root(),"src", "datasets","maptask","maptask.py")
print(DATASET_LOADING_SCRIPT)

def load_maptask(variant="default"):
    """Load and return the maptask dataset"""
    dataset = load_dataset(DATASET_LOADING_SCRIPT,name=variant)
    return dataset
