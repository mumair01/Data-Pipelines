# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-19 16:30:59
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-06-07 12:01:03


# All dataset packages must export a loader function and a list of supported
# variants
from data_pipelines.datasets.callhome.loader import (
    load_callhome,
    VARIANTS,
    DETAILS,
)
