# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-22 11:56:49
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-26 14:16:14

import os
from datasets import load_dataset

from data_pipelines.utils import get_module_path

_DATASET_LOADING_SCRIPT = os.path.join(
    get_module_path(), "datasets","fisher","fisher.py")
_VARIANTS = ("default", "audio")

def load_fisher(variant="default",**kwargs):
    """
    Obtain the fisher corpus
    Args:
        variant (str): Variant of the corpus. One of: "default", "audio"
    NOTE: Accepts all huggingface load_dataset kwargs: https://huggingface.co/docs/datasets/package_reference/loading_methods
    """
    assert variant in _VARIANTS, \
        f"Variant must be one of: {_VARIANTS}"

    kwargs.update({
        "name" : variant,
    })
    dataset = load_dataset(_DATASET_LOADING_SCRIPT,**kwargs)
    return dataset