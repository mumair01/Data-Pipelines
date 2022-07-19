# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-14 13:20:45
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-19 12:52:46

import pytest
from datasets import load_dataset

from data_pipelines.datasets.maptask import load_maptask


def test_maptask():
    dataset = load_maptask(variant="audio")
    print(dataset)
    print(dataset['train'][0])