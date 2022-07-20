# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-20 13:54:27
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-20 19:40:14

import pytest
from datasets import load_dataset

from data_pipelines.datasets.switchboard import load_switchboard
from data_pipelines.datasets.switchboard.isip import ISIPAlignedCorpusReader

def test_switchboard():
    # LOAD_SCRIPT = "/Users/muhammadumair/Documents/Repositories/mumair01-repos/Data-Pipelines/data_pipelines/datasets/switchboard/switchboard.py"
    # load_dataset(LOAD_SCRIPT,name="ISIP-word")
    # reader = ISIPAlignedCorpusReader("/Users/muhammadumair/.cache/huggingface/datasets/downloads/extracted/75d5f9aa54fa5a82caf150f029bda27864394e4335e2a8fffb22d3a0cf02c0b6")
    # trans = reader.get_session_transcript('4501','A')
    # print(reader.get_vocabulary())
    dataset = load_switchboard(variant="swda")
    print(dataset['train'][0])