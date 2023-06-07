# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-11 17:55:59
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-06-07 11:20:53

# All dataset packages must export a loader function and a list of supported
# variants
from data_pipelines.datasets.maptask.loader import (
    load_maptask,
    VARIANTS,
    DETAILS,
)
