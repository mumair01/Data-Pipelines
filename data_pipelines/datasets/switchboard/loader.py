# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-20 13:06:00
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-20 19:42:13


import os
from datasets import load_dataset

from data_pipelines.utils import get_module_path
from data_pipelines.datasets.maptask.maptask import MapTask

DATASET_LOADING_SCRIPT = os.path.join(
    get_module_path(), "datasets","switchboard","switchboard.py")

_VARIANTS = ('isip-aligned', 'swda')

def load_switchboard(variant="isip-aligned"):
    """Load and return the switchboard dataset"""
    assert variant in _VARIANTS,\
        f"Variant must be one of {_VARIANTS}"
    if variant == 'swda':
        dataset = load_dataset('swda')
    else:
        dataset = load_dataset(DATASET_LOADING_SCRIPT,name=variant)
    return dataset
