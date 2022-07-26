# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-21 16:23:19
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-26 15:20:51


import pytest

from data_pipelines.datasets.callfriend import load_callfriend
from data_pipelines.datasets import load_data

def test_callfriend():
    dataset = load_data(
        dataset="callfriend",
        variant="default",
        language="eng"
    )
    # dataset = load_callfriend(variant="default")
    print(dataset['full'][0])