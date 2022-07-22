# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-22 13:31:18
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-22 13:56:44


import pytest
from datasets import load_dataset

from data_pipelines.datasets.fisher.readers import (
    LDCTranscriptsReader
)


def test_fisher():
    TRANSCRIPTS_ROOT = "/Users/muhammadumair/Desktop/fe_03_p1_tran"
    LOAD_SCRIPT = "/Users/muhammadumair/Documents/Repositories/mumair01-repos/Data-Pipelines/data_pipelines/datasets/fisher/fisher.py"
    # reader = LDCTranscriptsReader(TRANSCRIPTS_ROOT)
    # #print(reader.get_sessions())
    # for session in reader.get_sessions():
    #     reader.get_session_transcript(session)
    load_dataset(LOAD_SCRIPT,name="default",data_dir=TRANSCRIPTS_ROOT)

