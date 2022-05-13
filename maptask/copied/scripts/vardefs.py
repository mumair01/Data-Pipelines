# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-05-08 16:01:46
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-10 09:57:01
import os
import re
import glob

# ---- Paths
# Dir paths.
PROJECT_ROOT_PATH = "/Users/muhammadumair/Documents/Repositories/mumair01-repos/Data-Pipelines/maptask/"
SCRIPTS_PATH = os.path.join(PROJECT_ROOT_PATH, "scripts")
SHELL_SCRIPTS_PATH = os.path.join(PROJECT_ROOT_PATH, "sh")
CONFIG_PATH = os.path.join(PROJECT_ROOT_PATH, "configs")
# NOTE: Make sure this is correct
OPENSMILE_PATH = os.path.join(PROJECT_ROOT_PATH, "opensmile-3.0.1-macos-x64")

# -- Script paths.

# Executables
AUDIO_WGET_SCRIPT_PATH = glob.glob(
    os.path.join(SHELL_SCRIPTS_PATH, "maptaskBuild*.sh"))[0]
OPENSMILE_EXE_PATH = os.path.join(OPENSMILE_PATH, "bin/SMILExtract")
# Configs
GEMAPS_10SEC_CONFIG = os.path.join(CONFIG_PATH, "gemaps_10ms/eGeMAPSv01a.conf")
GEMAPS_50SEC_CONFIG = os.path.join(CONFIG_PATH, "gemaps_50ms/eGeMAPSv01a.conf")


# ---- URLs
# NOTE: This is the link to the main zip file from: https://groups.inf.ed.ac.uk/maptask/maptasknxt.html
ANNOTATIONS_URL = "http://groups.inf.ed.ac.uk/maptask/hcrcmaptask.nxtformatv2-1.zip"


# -- Literals
DATASET_NAME = "maptask"
