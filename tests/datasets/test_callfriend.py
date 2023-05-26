# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-21 16:23:19
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-05-23 11:20:27


import pytest

from data_pipelines.datasets.callfriend import load_callfriend
from data_pipelines.datasets import load_data


def test_callfriend():
    dataset = load_data(dataset="callfriend", variant="audio", language="deu")
    # dataset = load_callfriend(variant="default")
    print(dataset["full"][0])
