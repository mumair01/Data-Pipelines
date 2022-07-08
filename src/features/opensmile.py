# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-07 16:44:55
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-08 14:11:39


import os
import subprocess
import opensmile
import audiofile
import argparse
import shutil
import pandas as pd
import glob

import torch

from src.features.utils import z_norm, z_norm_non_zero


def extract_gemaps_from_maptask_audio(
        audio_dir_path, output_dir, config_path):
    """
    Read all the wav files from a directory and extract their features based on
    the given configurations.
    Extracts the features using SMILExtract
    NOTE: Only .wav files are supported
    NOTE: opensmile must be downloaded and added to path : https://audeering.github.io/opensmile/get-started.html#default-feature-sets
    """
    assert os.path.isdir(audio_dir_path)
    os.makedirs(output_dir,exist_ok=True)
    assert os.path.isfile(config_path)
    config_name = os.path.splitext(os.path.basename(config_path))[0]
    # Read all wav files
    audio_paths = glob.glob("{}/*.wav".format(audio_dir_path))
    for audio_path in audio_paths:
        filename, ext = os.path.splitext(os.path.basename(audio_path))
        dialogue, participant = filename.split(".")
        if ext == ".wav":
            csv_path =os.path.join(output_dir,
                "{}.{}.{}.csv".format(dialogue,participant,config_name))
            cmd = "SMILExtract -C {} -I {} -D {}".format(
                config_path,audio_path,csv_path)
            subprocess.run(cmd, shell=True)


class OpenSmile:

    FEATURE_SETS = ["egemapsv02",]

    def __init__(self, feature_set="egemapsv02",
            feature_level="lld",
            sample_rate=16_000, normalize=False):
        self.feature_set = feature_set
        self.sample_rate = sample_rate
        self.normalize = normalize
        feature_set = self.get_feature_set(feature_set)
        self.smile = opensmile.Smile(
            feature_set=feature_set,
            feature_level=feature_level)


    @property
    def feat2idx(self):
        return {k: idx for idx, k in enumerate(self.smile.feature_names)}

    @property
    def idx2feat(self):
        return {idx: k for idx, k in enumerate(self.smile.feature_names)}

    @property
    def feature_names(self):
        return self.smile.feature_names

    def get_feature_set(self, feature_set):
        # Read the conf if the feature level is a file
        if os.path.isfile(feature_set) and \
                os.path.splitext(os.path.basename(feature_set))[1] == ".conf":
            return feature_set
        # Otherwise, check given sets.
        feature_set = feature_set.lower()
        assert (
            feature_set in self.FEATURE_SETS
        ), f"{feature_set} not found. Try {self.FEATURE_SETS}"

        if feature_set == "egemapsv02":
            return opensmile.FeatureSet.eGeMAPSv02
        elif feature_set == "emobase":
            return opensmile.FeatureSet.emobase
        else:
            raise NotImplementedError()

    def __repr__(self):
        return str(self.smile)

    def __call__(self, waveform):
        data =self.smile.process_signal(waveform, self.sample_rate)
        data.to_csv("/Users/muhammadumair/Documents/Repositories/mumair01-repos/Data-Pipelines/tests/features/test.csv")
        f = torch.from_numpy(
            data.to_numpy()
        )
        if self.normalize:
            fr = z_norm(f[..., self.idx_reg])
            fs = z_norm_non_zero(f[..., self.idx_special])
            f[..., self.idx_reg] = fr
            f[..., self.idx_special] = fs

        if waveform.ndim == 2:
            f = f.unsqueeze(0)
        return f









