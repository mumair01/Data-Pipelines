# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-20 11:52:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-26 16:06:19

import os
from datasets import load_dataset

from data_pipelines.utils import get_module_path

_DATASET_LOADING_SCRIPT = os.path.join(
    get_module_path(), "datasets","maptask","maptask.py")

_VARIANTS = ("default", "audio")

def load_maptask(variant="default",**kwargs):
    """
    Obtain the maptask corpus
    Args:
        variant (str): Variant of the corpus. One of: "default", "audio"
    """
    assert variant in _VARIANTS, \
        f"Variant must be one of: {_VARIANTS}"
    dataset = load_dataset(_DATASET_LOADING_SCRIPT,name=variant,**kwargs)
    return dataset
