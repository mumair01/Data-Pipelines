# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-20 11:49:49
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-05-23 10:06:53


import os
from datasets import load_dataset


from data_pipelines.paths import PkgPaths

_DATASET_LOADING_SCRIPT = os.path.join(
    PkgPaths.Core.datasetsMod, "callhome", "callhome.py"
)

_VARIANTS = ("default", "audio")
_LANGUAGES = "ara", "deu", "eng", "jpn", "spa", "zho"


def load_callhome(variant="default", language="eng", **kwargs):
    """
    Obtain the Callhome corpus with of the specified variant and language.
    NOTE: Accepts all huggingface load_dataset kwargs: https://huggingface.co/docs/datasets/package_reference/loading_methods
    Args:
        variant (str): Flavor of the dataset to load. One of: "default", "audio"
        language (str):  Callfriend corpus language.
            One of:  'ara','deu','eng','jpn','spa','zho'
    """
    assert language in _LANGUAGES, f"Language must be one of: {_LANGUAGES}"
    assert variant in _VARIANTS, f"Variant must be one of: {_VARIANTS}"

    kwargs.update({"name": variant, "language": language})
    dataset = load_dataset(_DATASET_LOADING_SCRIPT, **kwargs)
    return dataset
