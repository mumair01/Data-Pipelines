# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-22 11:56:49
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-06-07 11:18:37

import os
from datasets import load_dataset

from data_pipelines.paths import PkgPaths

_DATASET_LOADING_SCRIPT = os.path.join(
    PkgPaths.Core.datasetsMod, "fisher", "fisher.py"
)


VARIANTS = ("default", "audio")

# Dictionary listing the details for this dataset that should be exposed to the
# user.
DETAILS = {
    "name": "Fisher",
    "variants": VARIANTS,
}


def load_fisher(variant="default", **kwargs):
    """
    Obtain the fisher corpus
    Args:
        variant (str): Variant of the corpus. One of: "default", "audio"
    NOTE: Accepts all huggingface load_dataset kwargs: https://huggingface.co/docs/datasets/package_reference/loading_methods
    """
    assert variant in VARIANTS, f"Variant must be one of: {VARIANTS}"

    kwargs.update(
        {
            "name": variant,
        }
    )
    dataset = load_dataset(_DATASET_LOADING_SCRIPT, **kwargs)
    return dataset
