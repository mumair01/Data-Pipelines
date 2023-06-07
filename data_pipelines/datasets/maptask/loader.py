# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-20 11:52:08
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-06-07 11:21:16

import os
from datasets import load_dataset

from data_pipelines.paths import PkgPaths

_DATASET_LOADING_SCRIPT = os.path.join(
    PkgPaths.Core.datasetsMod, "maptask", "maptask.py"
)

VARIANTS = ("default", "audio")

# Dictionary listing the details for this dataset that should be exposed to the
# user.
DETAILS = {
    "name": "Maptask",
    "variants": VARIANTS,
}


def load_maptask(variant="default", **kwargs):
    """
    Obtain the maptask corpus
    Args:
        variant (str): Variant of the corpus. One of: "default", "audio"
    """
    assert variant in VARIANTS, f"Variant must be one of: {VARIANTS}"
    dataset = load_dataset(_DATASET_LOADING_SCRIPT, name=variant, **kwargs)
    return dataset
