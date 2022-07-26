# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-20 13:06:00
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-26 14:32:25


import os
from datasets import load_dataset

from data_pipelines.utils import get_module_path
from data_pipelines.datasets.maptask.maptask import MapTask

_DATASET_LOADING_SCRIPT = os.path.join(
    get_module_path(), "datasets","switchboard","switchboard.py")

_VARIANTS = ('isip-aligned', 'swda','ldc-audio')

def load_switchboard(variant="isip-aligned",**kwargs):
    """
    Load and return the switchboard dataset
     Args:
        variant (str): Variant of the corpus. One of: 'isip-aligned', 'swda','ldc-audio'
    NOTE: Accepts all huggingface load_dataset kwargs: https://huggingface.co/docs/datasets/package_reference/loading_methods
    """
    assert variant in _VARIANTS,\
        f"Variant must be one of {_VARIANTS}"
    if variant == 'swda':
        dataset = load_dataset('swda',**kwargs)
    else:
        dataset = load_dataset(_DATASET_LOADING_SCRIPT,name=variant,**kwargs)
    return dataset
