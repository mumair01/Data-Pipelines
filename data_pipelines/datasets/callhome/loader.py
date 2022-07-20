# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-20 11:49:49
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-20 11:49:59


import os
from datasets import load_dataset


from data_pipelines.utils import get_module_path
from data_pipelines.datasets.callhome.callhome import CallHome

DATASET_LOADING_SCRIPT = os.path.join(
    get_module_path(), "datasets","callhome","callhome.py")

def load_callhome(variant="default",language="eng",force_redownload=False):
    kwargs = {
        "name" : variant,
        "language" : language,
        "download_mode" : "reuse_dataset_if_exists" \
            if not force_redownload else "force_redownload"
    }
    dataset = load_dataset(DATASET_LOADING_SCRIPT,**kwargs)
    return dataset
