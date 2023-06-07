# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-05-23 09:29:23
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-06-07 11:48:19


"""
Manages the paths for the datasets module internally. 
"""

import os
import sys
from pathlib import Path
import json
from dataclasses import dataclass, asdict

#### Root paths
# Path to the root of the repo.
_ROOT_PATH = os.path.dirname(os.path.dirname(__file__))
# Path to the data_pipelines package
_MODULE_PATH = os.path.dirname(__file__)
# Directory used to cache datasets.
_CACHE_ROOT = os.path.join(os.path.expanduser("~"), ".cache/data_pipelines")
_CACHE_DIR = os.path.join(
    os.path.expanduser("~"), ".cache/data_pipelines/datasets"
)
# Directory used to store temporary files when downloading datasets.
_DOWNLOADS_DIR = os.path.join(_CACHE_ROOT, "downloads")
# Path to the configuration directory, which contains, amongst other things,
# configs for the opensmile package.
_CONFIGS_DIR = os.path.join(_MODULE_PATH, "configs")
# Path to the directory containing executables and shell scripts.
_BIN_DIR = os.path.join(_MODULE_PATH, "bin")


#### Exe paths

# Path to the appropriate sph2pipe file used by opensmile, depending on the
# platform being used.
if sys.platform == "darwin":
    # NOTE: This is the MAC OSX compiled binary for shp2pipe
    _SPH2PIPE_EXE_PATH = os.path.join(_BIN_DIR, "sph2pipe_osx")
elif sys.platform == "linux":
    _SPH2PIPE_EXE_PATH = os.path.join(_BIN_DIR, "sph2pipe")

#### Feature conf paths
# Path to the egemaps v2 configs used by opensmile.
_EGEMAPS_V02_50MS_CONF = os.path.join(
    _CONFIGS_DIR,
    "opensmile/pyopensmile/egemaps_v02_custom/egemaps_v02_50ms/eGeMAPSv02.conf",
)


@dataclass
class PkgPaths:
    """
    Dataclass containing core paths, executable paths, and egemaps configuration
    paths.
    """

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
