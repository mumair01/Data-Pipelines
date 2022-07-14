# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-07 17:01:31
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-11 16:41:06


import pytest
import torch
import librosa
import audiofile
import pandas


from src.features.opensmile import OpenSmile, extract_gemaps_from_maptask_audio


def test_opensmile_egemapsv02():
    MONO_AUDIO_FILE_PATH = "/Users/muhammadumair/Documents/Repositories/mumair01-repos/Data-Pipelines/data/corpora/maptaskv2-1/Data/signals/mono_signals/q1ec1.f.wav"
    CONF_PATH = "/Users/muhammadumair/Documents/Repositories/mumair01-repos/Data-Pipelines/configs/opensmile/pyopensmile/egemaps_v02_custom/egemaps_v02_50ms/eGeMAPSv02.conf"
    # Read the file
    signal, sampling_rate = audiofile.read(MONO_AUDIO_FILE_PATH,always_2d=True)
    print(audiofile.duration(MONO_AUDIO_FILE_PATH))
    smile = OpenSmile(feature_set=CONF_PATH,feature_level="lld",sample_rate=sampling_rate)
    # f = smile(signal)
    # print(f)