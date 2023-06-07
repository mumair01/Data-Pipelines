# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-19 16:30:59
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-06-07 11:09:16


from data_pipelines.datasets.callhome.loader import load_callhome
from dataclasses import dataclass


# All dataset packages must export a loader function and a list of supported
# variants
from data_pipelines.datasets.callhome.loader import (
    load_callfriend,
    VARIANTS,
    DETAILS,
)


@dataclass
class CallhomeVariants:
    DEFAULT: str = "default"
    AUDIO: str = "audio"
