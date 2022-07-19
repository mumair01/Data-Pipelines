# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-18 17:17:53
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-18 17:18:58


import os
import sys

def get_module_root():
    """
    Returns the absolute path to the src module.
    """
    root = os.path.dirname(__file__)
    root = os.path.dirname(root)
    return root