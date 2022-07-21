# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-18 17:17:53
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-21 11:54:22


import os
import sys
from pathlib import Path

############################### GENERAL METHODS #############################

def get_module_root():
    """
    Returns the absolute path to the src module.
    """
    root = os.path.dirname(__file__)
    root = os.path.dirname(root)
    return root

def get_module_path():
    return os.path.dirname(__file__)

