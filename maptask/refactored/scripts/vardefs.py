# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-05-11 14:46:20
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-12 16:31:14

import os
import re
import glob


# ---- Paths
# Dir paths.
PROJECT_ROOT_PATH = "/Users/muhammadumair/Documents/Repositories/mumair01-repos/Data-Pipelines/maptask/refactored"
SCRIPTS_PATH = os.path.join(PROJECT_ROOT_PATH, "scripts")
SHELL_SCRIPTS_PATH = os.path.join(PROJECT_ROOT_PATH, "sh")
CONFIG_PATH = os.path.join(PROJECT_ROOT_PATH, "configs")
PACKAGES_PATH = os.path.join(PROJECT_ROOT_PATH, "packages")
# NOTE: Make sure this is correct
OPENSMILE_PATH = os.path.join(PACKAGES_PATH, "opensmile-3.0.1-macos-x64")

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


# ---- Feature vars
# Constants
FREQUENCY_FEATURES = ['F0semitoneFrom27.5Hz', 'jitterLocal', 'F1frequency',
                      'F1bandwidth', 'F2frequency', 'F3frequency']
FREQUENCY_MASK = [0, 0, 0, 0, 0, 0]
ENERGY_FEATURES = ['Loudness', 'shimmerLocaldB', 'HNRdBACF']
ENERGY_MASK = [0, 0, 0]
SPECTRAL_FEATURES = ['alphaRatio', 'hammarbergIndex', 'spectralFlux',
                     'slope0-500', 'slope500-1500', 'F1amplitudeLogRelF0',
                     'F2amplitudeLogRelF0', 'F3amplitudeLogRelF0', 'mfcc1',
                     'mfcc2', 'mfcc3', 'mfcc4']
SPECTRAL_MASK = [0, 0, 0, 0, 0, -201, -201, -201, 0, 0, 0, 0]
GEMAP_FULL_FEATURES = FREQUENCY_FEATURES + ENERGY_FEATURES + SPECTRAL_FEATURES
