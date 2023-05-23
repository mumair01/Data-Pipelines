# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-20 13:05:13
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-05-23 13:04:18

from data_pipelines.datasets.switchboard.loader import load_switchboard
from dataclasses import dataclass


@dataclass
class SwitchboardVariants:
    ISIP_ALIGNED: str = "isip-aligned"
    LDC_AUDIO: str = "ldc_audio"
