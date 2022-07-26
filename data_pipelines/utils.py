# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-18 17:17:53
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-26 14:49:17


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
    """Obtain the path of the module"""
    return os.path.dirname(__file__)

