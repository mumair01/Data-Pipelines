# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-26 14:45:40
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-26 14:48:27

from data_pipelines.datasets.callfriend import load_callfriend
from data_pipelines.datasets.callhome import load_callhome
from data_pipelines.datasets.fisher import load_fisher
from data_pipelines.datasets.maptask import load_maptask
from data_pipelines.datasets.switchboard import load_switchboard

_LOADERS = {
    "callfriend" : load_callfriend,
    "callhome" : load_callhome,
    "fisher" : load_fisher,
    "maptask" : load_maptask,
    "switchboard" : load_switchboard
}

def load_data(dataset,**kwargs):
    """Central method for loading various datasets"""
    assert dataset in _LOADERS, \
         f"dataset must be one of: {list(_LOADERS.keys())}"
    return _LOADERS[dataset](**kwargs)