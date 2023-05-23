# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-22 11:56:49
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-05-23 13:02:11


from data_pipelines.datasets.fisher.loader import load_fisher
from dataclasses import dataclass


@dataclass
class FisherVariants:
    DEFAULT: str = "default"
    AUDIO: str = "audio"
