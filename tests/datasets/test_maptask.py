# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-14 13:20:45
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-14 13:54:17




import pytest
from datasets import load_dataset


from src.datasets.maptask.maptask import MapTask


def test_maptask():
    load_dataset("/Users/muhammadumair/Documents/Repositories/mumair01-repos/Data-Pipelines/src/datasets/maptask/maptask.py",download_mode="force_redownload")
