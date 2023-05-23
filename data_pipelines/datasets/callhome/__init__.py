# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-19 16:30:59
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-05-23 13:01:48


from data_pipelines.datasets.callhome.loader import load_callhome
from dataclasses import dataclass


@dataclass
class CallhomeVariants:
    DEFAULT: str = "default"
    AUDIO: str = "audio"
