# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-05-17 15:17:49
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-19 14:39:43

import argparse
from cgitb import reset
from dataclasses import dataclass
from re import L
import tqdm
import glob
import shutil
import subprocess
import os
from data_pipelines.datasets.utils import download_from_url, download_zip_from_url,\
                                extract_from_zip, stereo_to_mono,reset_dir


@dataclass
class DownloadPaths:
    """
    Stores the download paths of the maptask corpus
    """
    annotations_path : str
    stereo_path : str
    mono_path : str


class MapTaskDownloader:
    """
    Utility for downloading both the annotations and dialogues for the maptask
    corpus
    """

    ANNOTATIONS_URL = "http://groups.inf.ed.ac.uk/maptask/hcrcmaptask.nxtformatv2-1.zip"
    STEREO_AUDIO_URL = "https://groups.inf.ed.ac.uk/maptask/signals/dialogues/"
    MAPTASK_VERSION = "maptaskv2-1"

    _DOWNLOAD_DIR = "."
    _ANNOTATIONS_DOWNLOAD_DIR = os.path.join(_DOWNLOAD_DIR,"annotations")
    _STEREO_OUTPUT_DIR = os.path.join(_DOWNLOAD_DIR,"signals","dialogues")
    _MONO_OUTPUT_DIR = os.path.join(_DOWNLOAD_DIR,"signals","monologues")
    # Temp dirs.
    _TEMP_DIR = os.path.join(_DOWNLOAD_DIR,"temp")
    _STEREO_TEMP_DIR = os.path.join(_TEMP_DIR,"signals","dialogues")
    _MONO_TEMP_DIR = os.path.join(_TEMP_DIR,"signals","monologues")

    _STEREO_AUDIO_FILENAMES = [
        "q1ec1.mix.wav",
        "q1ec2.mix.wav",
        "q1ec3.mix.wav",
        "q1ec4.mix.wav",
        "q1ec5.mix.wav",
        "q1ec6.mix.wav",
        "q1ec7.mix.wav",
        "q1ec8.mix.wav",
        "q1nc1.mix.wav",
        "q1nc2.mix.wav",
        "q1nc3.mix.wav",
        "q1nc4.mix.wav",
        "q1nc5.mix.wav",
        "q1nc6.mix.wav",
        "q1nc7.mix.wav",
        "q1nc8.mix.wav",
        "q2ec1.mix.wav",
        "q2ec2.mix.wav",
        "q2ec3.mix.wav",
        "q2ec4.mix.wav",
        "q2ec5.mix.wav",
        "q2ec6.mix.wav",
        "q2ec7.mix.wav",
        "q2ec8.mix.wav",
        "q2nc1.mix.wav",
        "q2nc2.mix.wav",
        "q2nc3.mix.wav",
        "q2nc4.mix.wav",
        "q2nc5.mix.wav",
        "q2nc6.mix.wav",
        "q2nc7.mix.wav",
        "q2nc8.mix.wav",
        "q3ec1.mix.wav",
        "q3ec2.mix.wav",
        "q3ec3.mix.wav",
        "q3ec4.mix.wav",
        "q3ec5.mix.wav",
        "q3ec6.mix.wav",
        "q3ec7.mix.wav",
        "q3ec8.mix.wav",
        "q3nc1.mix.wav",
        "q3nc2.mix.wav",
        "q3nc3.mix.wav",
        "q3nc4.mix.wav",
        "q3nc5.mix.wav",
        "q3nc6.mix.wav",
        "q3nc7.mix.wav",
        "q3nc8.mix.wav",
        "q4ec1.mix.wav",
        "q4ec2.mix.wav",
        "q4ec3.mix.wav",
        "q4ec4.mix.wav",
        "q4ec5.mix.wav",
        "q4ec6.mix.wav",
        "q4ec7.mix.wav",
        "q4ec8.mix.wav",
        "q4nc1.mix.wav",
        "q4nc2.mix.wav",
        "q4nc3.mix.wav",
        "q4nc4.mix.wav",
        "q4nc5.mix.wav",
        "q4nc6.mix.wav",
        "q4nc7.mix.wav",
        "q4nc8.mix.wav",
        "q5ec1.mix.wav",
        "q5ec2.mix.wav",
        "q5ec3.mix.wav",
        "q5ec4.mix.wav",
        "q5ec5.mix.wav",
        "q5ec6.mix.wav",
        "q5ec7.mix.wav",
        "q5ec8.mix.wav",
        "q5nc1.mix.wav",
        "q5nc2.mix.wav",
        "q5nc3.mix.wav",
        "q5nc4.mix.wav",
        "q5nc5.mix.wav",
        "q5nc6.mix.wav",
        "q5nc7.mix.wav",
        "q5nc8.mix.wav",
        "q6ec1.mix.wav",
        "q6ec2.mix.wav",
        "q6ec3.mix.wav",
        "q6ec4.mix.wav",
        "q6ec5.mix.wav",
        "q6ec6.mix.wav",
        "q6ec7.mix.wav",
        "q6ec8.mix.wav",
        "q6nc1.mix.wav",
        "q6nc2.mix.wav",
        "q6nc3.mix.wav",
        "q6nc4.mix.wav",
        "q6nc5.mix.wav",
        "q6nc6.mix.wav",
        "q6nc7.mix.wav",
        "q6nc8.mix.wav",
        "q7ec1.mix.wav",
        "q7ec2.mix.wav",
        "q7ec3.mix.wav",
        "q7ec4.mix.wav",
        "q7ec5.mix.wav",
        "q7ec6.mix.wav",
        "q7ec7.mix.wav",
        "q7ec8.mix.wav",
        "q7nc1.mix.wav",
        "q7nc2.mix.wav",
        "q7nc3.mix.wav",
        "q7nc4.mix.wav",
        "q7nc5.mix.wav",
        "q7nc6.mix.wav",
        "q7nc7.mix.wav",
        "q7nc8.mix.wav",
        "q8ec1.mix.wav",
        "q8ec2.mix.wav",
        "q8ec3.mix.wav",
        "q8ec4.mix.wav",
        "q8ec5.mix.wav",
        "q8ec6.mix.wav",
        "q8ec7.mix.wav",
        "q8ec8.mix.wav",
        "q8nc1.mix.wav",
        "q8nc2.mix.wav",
        "q8nc3.mix.wav",
        "q8nc4.mix.wav",
        "q8nc5.mix.wav",
        "q8nc6.mix.wav",
        "q8nc7.mix.wav",
        "q8nc8.mix.wav",
    ]

    def __init__(self, output_dir : str, force_download : bool = False):
        """
        Args:
            output_dir (str):
                Directory containing the corpus. If output_dir already exists, it
                is assumed that it is a cached copy.
            force_download (bool):
                Set True to re-download even if output_dir exists.
        """
        # Create the dirs
        self.download_dir = os.path.join(output_dir,self._DOWNLOAD_DIR)
        self.temp_dir = os.path.join(output_dir,self._TEMP_DIR)
        # Output directories
        self.annotations_dir = os.path.join(
            self.download_dir,self._ANNOTATIONS_DOWNLOAD_DIR)
        self.stereo_dialogues_dir = os.path.join(
            self.download_dir,self._STEREO_OUTPUT_DIR)
        self.mono_dialogues_dir = os.path.join(
            self.download_dir,self._MONO_OUTPUT_DIR)
        # Assumes that if the output dir exists, it must be the corpus and
        # verifies integrity.
        if os.path.isdir(self.download_dir):
            if not self.__verify() and not force_download:
                raise Exception(f'ERROR: Integrity could not be verified {output_dir}')
            if force_download:
                for dir in (self.annotations_dir,self.stereo_dialogues_dir,self.mono_dialogues_dir):
                    if os.path.isdir(dir):
                        shutil.rmtree(dir)
        self.cached = os.path.isdir(self.download_dir) and not force_download

    def __call__(self):
        """
        Downloads the annotations and signals and returns paths
        to annotations, stereo, and mono dialogues.
        """
        if not self.cached:
            self.__download_annotations()
            self.__download_signals(extract_mono=True)
        return DownloadPaths(
            os.path.join(self.annotations_dir,self.MAPTASK_VERSION),
            self.stereo_dialogues_dir, self.mono_dialogues_dir)

    def __download_annotations(self):
        os.makedirs(self.annotations_dir,exist_ok=True)
        download_zip_from_url(self.ANNOTATIONS_URL,self.annotations_dir)

    def __download_signals(self,extract_mono=True):
        # Reset dirs.
        stereo_temp_path = os.path.join(self.temp_dir, self._STEREO_TEMP_DIR)
        mono_temp_path = os.path.join(self.temp_dir,self._MONO_TEMP_DIR)
        for dir in (self.temp_dir,stereo_temp_path, mono_temp_path):
            reset_dir(dir)
        # Download each file individually.
        for audiofile in self._STEREO_AUDIO_FILENAMES:
            url = os.path.join(self.STEREO_AUDIO_URL, audiofile)
            download_from_url(url,"{}/{}".format(stereo_temp_path,audiofile))
        stereo_paths = glob.glob("{}/*".format(stereo_temp_path))
        # Extract mono audios.
        if extract_mono:
            for stereo_path in stereo_paths:
                stereo_to_mono(stereo_path,mono_temp_path,left_prefix="g",
                                    right_prefix="f")
            shutil.move(mono_temp_path,self.mono_dialogues_dir)
        shutil.move(stereo_temp_path,self.stereo_dialogues_dir)
        shutil.rmtree(self.temp_dir)

    def __verify(self) -> bool:
        """
        Verify that the downloaded annotations and signals directories
        are complete.
        """
        # Check that the annotations dir exists.
        return os.path.isdir(self.annotations_dir) and \
            os.path.isdir(self.stereo_dialogues_dir) and \
            os.path.isdir(self.mono_dialogues_dir) and \
            len(os.listdir(self.mono_dialogues_dir)) == 2 \
                    * len(os.listdir(self.stereo_dialogues_dir))
