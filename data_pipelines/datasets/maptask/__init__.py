# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-11 17:55:59
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-05-23 13:02:49

from data_pipelines.datasets.maptask.loader import load_maptask
from dataclasses import dataclass


@dataclass
class MaptaskVariants:
    DEFAULT: str = "default"
    AUDIO: str = "audio"
