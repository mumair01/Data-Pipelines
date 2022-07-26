# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-19 14:50:11
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-26 15:11:48


import pytest

from data_pipelines.datasets import load_data
from data_pipelines.datasets.callhome import load_callhome

def test_callhome():
    dataset = load_data(
        dataset="callhome",
        variant="default",
        language="eng"
    )
    # dataset = load_callfriend(variant="default")
    print(dataset['all'][0])

