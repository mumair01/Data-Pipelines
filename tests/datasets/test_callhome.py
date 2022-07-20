# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-19 14:50:11
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-20 11:56:51


import pytest

from data_pipelines.datasets.callhome import load_callhome

def test_daily_dialog():
    dataset = load_callhome(language="ara",variant="default",force_redownload=False)
    print(dataset['train'][1])
    # for item in dataset['train']:
    #     print(item['id'])
    #     for utt in item['utterances']:
    #         print(utt)