# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-20 13:06:00
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-05-23 10:05:46


import os
from datasets import load_dataset

from data_pipelines.paths import PkgPaths
from data_pipelines.datasets.maptask.maptask import MapTask

_DATASET_LOADING_SCRIPT = os.path.join(
    PkgPaths.Core.datasetsMod, "switchboard", "switchboard.py"
)

_VARIANTS = ("isip-aligned", "swda", "ldc-audio")


def load_switchboard(variant="isip-aligned", **kwargs):
    """
    Load and return the switchboard dataset
     Args:
        variant (str): Variant of the corpus. One of: 'isip-aligned', 'swda','ldc-audio'
    NOTE: Accepts all huggingface load_dataset kwargs: https://huggingface.co/docs/datasets/package_reference/loading_methods
    """
    assert variant in _VARIANTS, f"Variant must be one of {_VARIANTS}"
    if variant == "swda":
        dataset = load_dataset("swda", **kwargs)
    else:
        dataset = load_dataset(_DATASET_LOADING_SCRIPT, name=variant, **kwargs)
    return dataset
