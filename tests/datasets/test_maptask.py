# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-14 13:20:45
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-05-23 10:10:14

import pytest
from datasets import load_dataset, load_from_disk
import numpy as np

from data_pipelines.datasets.maptask import load_maptask
from data_pipelines.features import OpenSmile, extract_feature_set
from data_pipelines.datasets import load_data


def test_maptask():
    # dataset = load_maptask(variant="audio")
    # # Can create the test splits
    dset = load_data(dataset="maptask", variant="audio")

    dset_splits = dset["full"].train_test_split(test_size=0.01)
    test_dset = dset_splits["test"]
    print(test_dset)

    def extract_gemaps(item):
        item["mono_gemaps"] = extract_feature_set(
            item["audio_paths"]["mono"], feature_set="egemapsv02_50ms"
        )
        return item

    test_dset = test_dset.map(extract_gemaps)
    test_dset.save_to_disk("./test_dset")

    test_dset = load_from_disk("./test_dset")
