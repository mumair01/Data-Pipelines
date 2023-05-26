# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-19 14:50:11
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-05-23 12:48:46


import pytest

from data_pipelines.datasets import load_data
from data_pipelines.datasets.callhome import load_callhome


def test_callhome():
    dataset = load_data(dataset="callhome", variant="audio", language="eng")
    # dataset = load_callfriend(variant="default")
    print(dataset["full"][0])
