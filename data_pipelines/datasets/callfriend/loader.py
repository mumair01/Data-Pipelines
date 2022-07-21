# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-21 16:23:45
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-21 16:45:57


import os
from datasets import load_dataset

from data_pipelines.utils import get_module_path

DATASET_LOADING_SCRIPT = os.path.join(
    get_module_path(), "datasets","callfriend","callfriend.py")

def load_callfriend(variant="default",language="eng-n",force_redownload=False):
    kwargs = {
        "name" : variant,
        "language" : language,
        "download_mode" : "reuse_dataset_if_exists" \
            if not force_redownload else "force_redownload"
    }
    dataset = load_dataset(DATASET_LOADING_SCRIPT,**kwargs)
    return dataset
