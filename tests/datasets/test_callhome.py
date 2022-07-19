# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-19 14:50:11
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-19 16:30:10


import pytest

from data_pipelines.datasets.callhome import load_callhome

def test_daily_dialog():
    load_callhome()