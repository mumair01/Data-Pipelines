# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-19 16:30:59
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-19 16:33:12


import os
from datasets import load_dataset

from data_pipelines.utils import get_module_path
from data_pipelines.datasets.callhome.callhome import CallHome

DATASET_LOADING_SCRIPT = os.path.join(
    get_module_path(), "datasets","callhome","callhome.py")

def load_callhome():
    dataset = load_dataset(DATASET_LOADING_SCRIPT)
    return dataset
