# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-07 16:44:55
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-11 16:48:45


import os
import subprocess
from matplotlib import use
import opensmile
import audiofile
import argparse
import shutil
import pandas as pd
import glob

import torch

from src.features.utils import z_norm, z_norm_non_zero


class OpenSmile:

    FEATURE_SETS = ["egemapsv02",]
    SMILE_EXTRACT_CMD = "SMILExtract -C {} -I {} -D {}"

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

    def _settings(self):
        if self.feature_set_name == "egemapsv02":
            self.pad_samples = int(self.sample_rate * 0.02)
            self.pad_frames = 2
            self.f0_idx = 10
            self.idx_special = [10, 13, 14, 15, 18, 21, 24]
            self.idx_reg = list(range(25))
            for ii in self.idx_special:
                self.idx_reg.pop(self.idx_reg.index(ii))

        elif self.feature_set_name == "emobase":
            self.pad_samples = int(self.sample_rate * 0.01)
            self.pad_frames = 1
            self.f0_idx = 24
            self.idx_special = [24, 25]
            self.idx_reg = list(range(26))
            for ii in self.idx_special:
                self.idx_reg.pop(self.idx_reg.index(ii))
        else:
            raise NotImplementedError()

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
        if self.use_smile_extract:
            pass
        else:
            data =self.smile.process_signal(waveform, self.sample_rate)
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

    def use_smile_extract(self, audio_path, output_dir):

        assert os.path.isdir(output_dir), "Output directory must exist"
        assert os.path.isfile(audio_path), "Audio path must exist"
        assert os.path.isfile(self.feature_set) and \
                os.path.splitext(os.path.basename(self.feature_set))[1] == ".conf", \
                    "Feature set must be a .conf configuration"
        filename, _ = os.path.splitext(os.path.basename(audio_path))
        csv_path =os.path.join(output_dir,
                "{}_{}.csv".format(
                    filename, os.path.splitext(os.path.basename(self.feature_set))))
        try:
            cmd = self.SMILE_EXTRACT_CMD.format(
                self.feature_set,audio_path,csv_path)
            subprocess.run(cmd, shell=True)
        except:
            pass





