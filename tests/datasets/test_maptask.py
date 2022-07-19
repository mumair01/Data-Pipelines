# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-14 13:20:45
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-18 17:21:25




import pytest
from datasets import load_dataset


from src.datasets.maptask import load_maptask


def test_maptask():
    dataset = load_maptask()
    print(dataset)
    for item in dataset['train']:
        print(item['dialogue'])
        print(item['participant'])
        print(item['audio_paths'])
        for utt in item['utterances']:
            print(utt)
        break