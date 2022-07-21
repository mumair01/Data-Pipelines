# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-21 16:23:19
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-21 16:45:35


import pytest

from data_pipelines.datasets.callfriend import load_callfriend

def test_callfriend():
    dataset = load_callfriend(variant="default")
    print(dataset['train'][0])