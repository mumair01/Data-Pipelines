# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-06-07 12:03:10
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-06-07 13:24:16

import pytest

import datasets
from datasets import load_from_disk
from data_pipelines.datasets import DataPipeline
import data_pipelines.features as dpf


_SAVE_DIR = "tests/test_results"


def test_dset_variants():
    dp = DataPipeline()
    datasets = dp.supported_dsets()
    for dataset in datasets:
        assert isinstance(dp.dset_variants(dataset), list)


def test_dset_details():
    dp = DataPipeline()
    datasets = dp.supported_dsets()
    for dataset in datasets:
        assert isinstance(dp.dset_details(dataset), dict)


def test_clear_cache():
    dp = DataPipeline()
    dp.clear_cache()


def test_load():
    dp = DataPipeline()
    datasets = dp.supported_dsets()
    for dataset in datasets:
        variants = dp.dset_variants(dataset)
        for variant in variants:
            dset = dp.load_dset(dataset=dataset, variant=variant)
            assert isinstance(dset, datasets.dataset_dict.DatasetDict)


def test_save_and_load_from_disk():
    dp = DataPipeline()
    datasets = dp.supported_dsets()
    for dataset in datasets:
        variants = dp.dset_variants(dataset)
        for variant in variants:
            dset = dp.load_dset(dataset=dataset, variant=variant)
            dset = dp.load_dset(dataset=dataset, variant=variant)
            dataset_path = f"{_SAVE_DIR}/{dataset}_{variant}"
            dset.save_to_disk(dataset_path)
            dset = load_from_disk(dataset_path)
            assert isinstance(dset, datasets.dataset_dict.DatasetDict)


def test_extract_audio_dset_features():
    def extract_gemaps(item):
        item["mono_gemaps"] = dpf.extract_feature_set(
            item["audio_paths"]["mono"], feature_set="egemapsv02_50ms"
        )
        return item

    dp = DataPipeline()
    dset = dp.load_dset(dataset="maptask", variant="audio")
    # Split the dataset and map on the smaller subset to save time.
    dset_splits = dset["full"].train_test_split(test_size=0.01)
    test_dset = dset_splits["test"]
    test_dset = test_dset.map(extract_gemaps)
