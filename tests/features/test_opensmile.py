# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-07 17:01:31
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-19 12:27:36


import pytest
import torch
import librosa
import audiofile
import pandas


from data_pipelines.features.opensmile import (
    OpenSmile
)


def test_opensmile_egemapsv02():
    MONO_AUDIO_FILE_PATH = "/Users/muhammadumair/Documents/Repositories/mumair01-repos/Data-Pipelines/data/corpora/maptaskv2-1/Data/signals/mono_signals/q1ec1.f.wav"
    # Read the file
    signal, sampling_rate = audiofile.read(MONO_AUDIO_FILE_PATH,always_2d=True)
    print(audiofile.duration(MONO_AUDIO_FILE_PATH))
    smile = OpenSmile(feature_set="egemapsv02_50ms",feature_level="lld",sample_rate=sampling_rate)
    f = smile(signal)
    print(smile.idx2feat)
    print(len(list(smile.idx2feat.keys())))
    print(f)
    print(f.shape)