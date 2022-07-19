# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-07 16:44:55
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-19 12:26:35


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

from data_pipelines.utils import get_module_path
from data_pipelines.features.utils import z_norm, z_norm_non_zero


_EGEMAPS_V02_50MS_CONF = os.path.join(
    get_module_path(),"configs/opensmile/pyopensmile/egemaps_v02_custom/egemaps_v02_50ms/eGeMAPSv02.conf")


class OpenSmile:

    _FEATURE_SETS = ["egemapsv02_default", "egemapsv02_50ms"]

    _SMILE_EXTRACT_CMD = "SMILExtract -C {} -I {} -D {}"

    def __init__(self, feature_set="egemapsv02_default",
            feature_level="lld",
            sample_rate=16_000, normalize=False,
            use_smile=False,):
        self.feature_set = feature_set
        self.sample_rate = sample_rate
        self.normalize = normalize
        self.use_smile = use_smile
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
        if self.feature_set_name == "egemapsv02_default" or \
                self.feature_set_name == "egemapsv02_50ms":
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
        feature_set = feature_set.lower()
        assert (
            feature_set in self._FEATURE_SETS
        ), f"{feature_set} not found. Try {self._FEATURE_SETS}"

        if feature_set == "egemapsv02_default":
            return opensmile.FeatureSet.eGeMAPSv02
        elif feature_set == "egemapsv02_50ms":
            assert os.path.isfile(_EGEMAPS_V02_50MS_CONF)
            return _EGEMAPS_V02_50MS_CONF
        elif feature_set == "emobase":
            return opensmile.FeatureSet.emobase
        else:
            raise NotImplementedError()

    def __repr__(self):
        return str(self.smile)

    def __call__(self, waveform):
        if self.use_smile:
            # TODO: Implement this at some point for compatibility.
            raise NotImplementedError()
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





