# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-20 13:54:27
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-21 15:42:19

import pytest
from datasets import load_dataset

from data_pipelines.datasets.switchboard import load_switchboard
from data_pipelines.datasets.switchboard.isip import ISIPAlignedCorpusReader
from data_pipelines.datasets.switchboard.ldc import LDCAudioCorpusReader

def test_switchboard():
    SWITCHBOARD_AUDIO_PATH = "/Users/muhammadumair/Documents/Research/Projects Data/Corpora/switchboard_swb1_LDC97S62"
    # LOAD_SCRIPT = "/Users/muhammadumair/Documents/Repositories/mumair01-repos/Data-Pipelines/data_pipelines/datasets/switchboard/switchboard.py"
    # load_dataset(LOAD_SCRIPT,name="ldc-audio",data_dir=SWITCHBOARD_AUDIO_PATH)
    # reader = ISIPAlignedCorpusReader("/Users/muhammadumair/.cache/huggingface/datasets/downloads/extracted/75d5f9aa54fa5a82caf150f029bda27864394e4335e2a8fffb22d3a0cf02c0b6")
    # trans = reader.get_session_transcript('4501','A')
    # print(reader.get_vocabulary())
    # dataset = load_switchboard(variant="swda")
    # print(dataset['train'][0])

    #reader = LDCAudioCorpusReader(SWITCHBOARD_AUDIO_PATH)
    # print(reader.disks)
    # print(reader.sph_paths)
    # print(reader.wav_paths)
    # print(reader.mono_paths)
    # print(reader.get_sessions())
    # load_switchboard(variant="ldc-audio",data_dir=SWITCHBOARD_AUDIO_PATH)
    # load_switchboard(variant="isip-aligned")
    # load_switchboard(variant="swda")
