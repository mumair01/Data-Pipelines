# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-20 11:52:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-05-23 10:06:13

import os
from datasets import load_dataset

from data_pipelines.paths import PkgPaths

_DATASET_LOADING_SCRIPT = os.path.join(
    PkgPaths.Core.datasetsMod, "maptask", "maptask.py"
)

_VARIANTS = ("default", "audio")


def load_maptask(variant="default", **kwargs):
    """
    Obtain the maptask corpus
    Args:
        variant (str): Variant of the corpus. One of: "default", "audio"
    """
    assert variant in _VARIANTS, f"Variant must be one of: {_VARIANTS}"
    dataset = load_dataset(_DATASET_LOADING_SCRIPT, name=variant, **kwargs)
    return dataset
