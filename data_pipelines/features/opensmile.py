# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-07 16:44:55
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-06-07 12:59:43


import os
import subprocess
from matplotlib import use
import opensmile
import audiofile
import torch
from typing import Dict

from data_pipelines.paths import PkgPaths
from data_pipelines.features.utils import z_norm, z_norm_non_zero


_EGEMAPS_V02_50MS_CONF = PkgPaths.Egemaps.v02_50ms_conf


class OpenSmile:
    """
    Class for using opensmile to extract audio features.
    Link: https://audeering.github.io/opensmile-python/
    """

    _FEATURE_SETS = ["egemapsv02_default", "egemapsv02_50ms"]

    _SMILE_EXTRACT_CMD = "SMILExtract -C {} -I {} -D {}"

    def __init__(
        self,
        feature_set="egemapsv02_default",
        feature_level="lld",
        sample_rate=16_000,
        normalize=False,
        use_smile=False,
    ):
        """
        Args:
            feature_set (str): Feature set to extract.
                One of: ["egemapsv02_default", "egemapsv02_50ms"]
            feature_level (str): Feature level to extract. One of: lld or func
            sample_rate (int)
            use_simle (bool):
                If True, use SmileExtract instead of OpenSmile. SmileExtract
                must be installed in this case.
                Link: https://www.audeering.com/research/opensmile/
        """
        self.feature_set = feature_set
        self.sample_rate = sample_rate
        self.normalize = normalize
        self.use_smile = use_smile
        feature_set = self.get_feature_set(feature_set)
        self.smile = opensmile.Smile(
            feature_set=feature_set, feature_level=feature_level
        )

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
        if (
            self.feature_set_name == "egemapsv02_default"
            or self.feature_set_name == "egemapsv02_50ms"
        ):
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
            data = self.smile.process_signal(waveform, self.sample_rate)
            f = torch.from_numpy(data.to_numpy())
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
        assert (
            os.path.isfile(self.feature_set)
            and os.path.splitext(os.path.basename(self.feature_set))[1]
            == ".conf"
        ), "Feature set must be a .conf configuration"
        filename, _ = os.path.splitext(os.path.basename(audio_path))
        csv_path = os.path.join(
            output_dir,
            "{}_{}.csv".format(
                filename, os.path.splitext(os.path.basename(self.feature_set))
            ),
        )
        try:
            cmd = self.SMILE_EXTRACT_CMD.format(
                self.feature_set, audio_path, csv_path
            )
            subprocess.run(cmd, shell=True)
        except:
            pass


def extract_feature_set(audio_path: str, feature_set: str) -> Dict:
    """
    Convenience method for extracting audio features of the given feature set.
    Use OpenSmile directly if this does not cover all cases
    """
    signal, sampling_rate = audiofile.read(audio_path, always_2d=True)
    smile = OpenSmile(
        feature_set=feature_set,
        feature_level="lld",
        sample_rate=sampling_rate,
        normalize=False,
    )
    f = smile(signal)
    return {"values": f, "features": list(smile.idx2feat.values())}
