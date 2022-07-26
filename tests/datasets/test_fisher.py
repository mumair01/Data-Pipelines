# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-22 13:31:18
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-26 15:20:47


import pytest
from datasets import load_dataset

from data_pipelines.datasets.fisher.readers import (
    LDCTranscriptsReader
)

from data_pipelines.datasets.fisher import load_fisher
from data_pipelines.datasets import load_data

def test_fisher():
    TRANSCRIPTS_ROOT = "/Users/muhammadumair/Desktop/fe_03_p1_tran"
    AUDIO_ROOT = "/Users/muhammadumair/Desktop/fisher_eng_tr_sp_LDC2004S13"
    LOAD_SCRIPT = "/Users/muhammadumair/Documents/Repositories/mumair01-repos/Data-Pipelines/data_pipelines/datasets/fisher/fisher.py"
    # reader = LDCTranscriptsReader(TRANSCRIPTS_ROOT)
    # #print(reader.get_sessions())
    # for session in reader.get_sessions():
    #     reader.get_session_transcript(session)
    #load_dataset(LOAD_SCRIPT,name="default",data_dir=TRANSCRIPTS_ROOT)
    # dataset = load_fisher(variant="audio",data_dir=AUDIO_ROOT)
    # print(dataset['train'][0])

    dataset = load_data(
        dataset="fisher",
        variant="default"
    )
    print(dataset['full'][0])