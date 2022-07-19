# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-19 14:22:58
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-19 14:25:19


import pytest

from data_pipelines.datasets.daily_dialogue import load_daily_dialog

def test_daily_dialog():
    dataset = load_daily_dialog()
    print(dataset['train']['dialog'][0])