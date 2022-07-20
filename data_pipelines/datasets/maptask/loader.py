# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-20 11:52:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-20 11:52:16

import os
from datasets import load_dataset

from data_pipelines.utils import get_module_path
from data_pipelines.datasets.maptask.maptask import MapTask

DATASET_LOADING_SCRIPT = os.path.join(
    get_module_path(), "datasets","maptask","maptask.py")

def load_maptask(variant="default"):
    """Load and return the maptask dataset"""
    dataset = load_dataset(DATASET_LOADING_SCRIPT,name=variant)
    return dataset
