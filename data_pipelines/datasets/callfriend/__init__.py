# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-21 16:23:45
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-06-06 11:03:05


# All dataset packages must export a loader function and a list of supported
# variants
from data_pipelines.datasets.callfriend.loader import (
    load_callfriend,
    VARIANTS,
    DETAILS,
)
