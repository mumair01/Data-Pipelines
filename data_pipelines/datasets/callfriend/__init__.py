# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-21 16:23:45
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-05-23 13:01:59

from data_pipelines.datasets.callfriend.loader import load_callfriend
from dataclasses import dataclass


@dataclass
class CallfriendVariants:
    DEFAULT: str = "default"
    AUDIO: str = "audio"
