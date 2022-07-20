# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-20 13:06:00
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-20 18:55:38


import os
from datasets import load_dataset

from data_pipelines.utils import get_module_path
from data_pipelines.datasets.maptask.maptask import MapTask

DATASET_LOADING_SCRIPT = os.path.join(
    get_module_path(), "datasets","switchboard","switchboard.py")

def load_switchboard(variant="default"):
    """Load and return the switchboard dataset"""
    dataset = load_dataset(DATASET_LOADING_SCRIPT,name=variant)
    return dataset
