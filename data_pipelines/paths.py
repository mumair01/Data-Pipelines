# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-05-23 09:29:23
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-05-23 10:03:54


import os
import sys
from pathlib import Path
import json
from dataclasses import dataclass, asdict

#### Root paths
_ROOT_PATH = os.path.dirname(os.path.dirname(__file__))
_MODULE_PATH = os.path.dirname(__file__)
_CACHE_DIR = os.path.join(
    os.path.expanduser("~"), ".cache/data_pipelines/datasets"
)
_DOWNLOADS_DIR = os.path.join(_CACHE_DIR, "downloads")
_CONFIGS_DIR = os.path.join(_ROOT_PATH, "configs")
_BIN_DIR = os.path.join(_ROOT_PATH, "bin")


#### Exe paths
if sys.platform == "darwin":
    # NOTE: This is the MAC OSX compiled binary for shp2pipe
    _SPH2PIPE_EXE_PATH = os.path.join(_BIN_DIR, "sph2pipe_osx")
elif sys.platform == "linux":
    _SPH2PIPE_EXE_PATH = os.path.join(_BIN_DIR, "sph2pipe")

#### Feature conf paths

_EGEMAPS_V02_50MS_CONF = os.path.join(
    _CONFIGS_DIR,
    "opensmile/pyopensmile/egemaps_v02_custom/egemaps_v02_50ms/eGeMAPSv02.conf",
)


@dataclass
class PkgPaths:
    @dataclass
    class Core:
        rootPath: str = _ROOT_PATH
        modulePath: str = _MODULE_PATH
        datasetsMod: str = os.path.join(_MODULE_PATH, "datasets")
        featuresMod: str = os.path.join(_MODULE_PATH, "features")
        cacheDir: str = _CACHE_DIR
        downloadDir: str = _DOWNLOADS_DIR

    @dataclass
    class Exe:
        sph2pipe: str = _SPH2PIPE_EXE_PATH

    @dataclass
    class Egemaps:
        v02_50ms_conf: str = _EGEMAPS_V02_50MS_CONF
