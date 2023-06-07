# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-08 15:59:39
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-06-06 10:45:08

import sys

# Package versioning information.
__author__ = "Muhammad Umair"
__version__ = "0.0.1a"
__email__ = "muhammad.umair@tufts.edu"

# Ensure that the appropriate platform is being used - only linux and mac
# currently supported.
_SUPPORTED_PLATFORMS = ("darwin", "linux")
_PLATFORM = sys.platform
if not _PLATFORM in _SUPPORTED_PLATFORMS:
    raise Exception(
        f"ERROR: Unsupported platform {_PLATFORM}, must be one of {_SUPPORTED_PLATFORMS}"
    )
