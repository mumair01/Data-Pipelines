# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-21 16:23:45
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-06-06 11:03:54


import os
from datasets import load_dataset, Dataset
from collections import namedtuple

from data_pipelines.paths import PkgPaths


# Path to the script that is run by load_dataset to load this dataset.
_DATASET_LOADING_SCRIPT = os.path.join(
    PkgPaths.Core.datasetsMod, "callfriend", "callfriend.py"
)

# Languages supported by the callfriend corpus
_LANGUAGES = (
    "deu",
    "eng-n",
    "eng-s",
    "fra-q",
    "jpn",
    "spa-c",
    "spa",
    "zho-m",
    "zho-t",
)

VARIANTS = ("default", "audio")

# Dictionary listing the details for this dataset that should be exposed to the
# user.
DETAILS = {
    "name": "Callfriend",
    "variants": VARIANTS,
    "additional kwargs": {"languages": _LANGUAGES},
}


def load_callfriend(
    variant: str = "default",
    language: str = "eng-n",
    **kwargs,
) -> Dataset:
    """
    Obtain the Callfriend corpus with of the specified variant and
    language.
    NOTE: Accepts all huggingface load_dataset kwargs: https://huggingface.co/docs/datasets/package_reference/loading_methods
    Args:
        variant (str): Flavor of the dataset to load. One of: "default", "audio"
        language (str):  Callfriend corpus language.
            One of: "deu",'eng-n','eng-s','fra-q','jpn','spa-c','spa','zho-m','zho-t'
    """
    assert language in _LANGUAGES, f"Language must be one of: {_LANGUAGES}"
    assert variant in VARIANTS, f"Variant must be one of: {VARIANTS}"

    kwargs.update({"name": variant, "language": language})
    dataset = load_dataset(_DATASET_LOADING_SCRIPT, **kwargs)
    return dataset
