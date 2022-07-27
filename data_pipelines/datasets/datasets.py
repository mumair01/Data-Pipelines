# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-26 14:45:40
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-27 09:38:36

import os
import glob
import shutil

from data_pipelines.datasets.callfriend import load_callfriend
from data_pipelines.datasets.callhome import load_callhome
from data_pipelines.datasets.fisher import load_fisher
from data_pipelines.datasets.maptask import load_maptask
from data_pipelines.datasets.switchboard import load_switchboard

from data_pipelines.datasets.utils import reset_dir


_LOADERS = {
    "callfriend" : load_callfriend,
    "callhome" : load_callhome,
    "fisher" : load_fisher,
    "maptask" : load_maptask,
    "switchboard" : load_switchboard
}

_CACHE_DIR = os.path.join(os.path.expanduser("~"),".cache/data_pipelines/datasets")
_DOWNLOADS_DIR = os.path.join(_CACHE_DIR,"downloads")



def load_data(dataset,**kwargs):
    """Central method for loading various datasets"""
    assert dataset in _LOADERS, \
         f"dataset must be one of: {list(_LOADERS.keys())}"
    # Specify the cache directory
    kwargs.update({
        "cache_dir" : _CACHE_DIR,
    })
    return _LOADERS[dataset](**kwargs)

def get_cache_dir():
    return _CACHE_DIR

def get_downloads_dir():
    return _DOWNLOADS_DIR