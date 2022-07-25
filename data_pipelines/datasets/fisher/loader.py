# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-22 11:56:49
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-25 15:53:30

import os
from datasets import load_dataset

from data_pipelines.utils import get_module_path

DATASET_LOADING_SCRIPT = os.path.join(
    get_module_path(), "datasets","fisher","fisher.py")

def load_fisher(variant="default", force_redownload=False,**kwargs):
    kwargs.update({
        "name" : variant,
        "download_mode" : "reuse_dataset_if_exists" \
            if not force_redownload else "force_redownload"
    })
    dataset = load_dataset(DATASET_LOADING_SCRIPT,**kwargs)
    return dataset