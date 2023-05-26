# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-26 14:45:40
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-05-23 10:07:56

import os
import glob
import shutil

from data_pipelines.datasets.callfriend import load_callfriend
from data_pipelines.datasets.callhome import load_callhome
from data_pipelines.datasets.fisher import load_fisher
from data_pipelines.datasets.maptask import load_maptask
from data_pipelines.datasets.switchboard import load_switchboard

from data_pipelines.datasets.utils import reset_dir
from data_pipelines.paths import PkgPaths


# NOTE: Candor and ICC are not yet supported.
_LOADERS = {
    "callfriend": load_callfriend,
    "callhome": load_callhome,
    "fisher": load_fisher,
    "maptask": load_maptask,
    "switchboard": load_switchboard,
}

_CACHE_DIR = PkgPaths.Core.cacheDir
_DOWNLOADS_DIR = PkgPaths.Core.downloadDir


def load_data(dataset, **kwargs):
    """Central method for loading various datasets"""
    assert (
        dataset in _LOADERS
    ), f"dataset must be one of: {list(_LOADERS.keys())}"
    # Specify the cache directory
    kwargs.update(
        {
            "cache_dir": _CACHE_DIR,
        }
    )
    return _LOADERS[dataset](**kwargs)


def get_cache_dir() -> str:
    """Provides the absolute path to the cache dir"""
    return _CACHE_DIR


def get_downloads_dir() -> str:
    """Provides the absolute path to the download dir"""
    return _DOWNLOADS_DIR
