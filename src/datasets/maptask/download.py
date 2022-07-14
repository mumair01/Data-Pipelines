# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-05-17 15:17:49
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-14 16:47:57

import argparse
import tqdm
import glob
import shutil
import subprocess
import os
from src.datasets.utils import download_from_url, download_zip_from_url,\
                                extract_from_zip, stereo_to_mono

# ---------------------------------- GLOBALS -----------------------------------

class MapTaskDownloader:

    DOWNLOAD_DIR = "."
    ANNOTATIONS_DOWNLOAD_DIR = os.path.join(DOWNLOAD_DIR,"annotations")
    STEREO_AUDIO_DIR = os.path.join(DOWNLOAD_DIR,"signals","dialogues")
    MONO_AUDIO_DIR = os.path.join(DOWNLOAD_DIR,"signals","mono_dialogues")
    TEMP_DIR = os.path.join(DOWNLOAD_DIR,"temp")

    ANNOTATIONS_URL = "http://groups.inf.ed.ac.uk/maptask/hcrcmaptask.nxtformatv2-1.zip"
    STEREO_AUDIO_URL = "https://groups.inf.ed.ac.uk/maptask/signals/dialogues/"

    STEREO_AUDIO_FILENAMES = [
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


    def __init__(self, output_dir : str):
        # Create the dirs
        self.download_dir = os.path.join(output_dir,self.DOWNLOAD_DIR)
        self.temp_dir = os.path.join(output_dir,self.TEMP_DIR)

    def __call__(self):
        annotations_path = self.download_annotations()
        stereo_output_path, mono_output_path = \
            self.download_signals(extract_mono=True)
        return (annotations_path, stereo_output_path, mono_output_path)


    def download_annotations(self):
        download_path = os.path.join(
            self.download_dir,self.ANNOTATIONS_DOWNLOAD_DIR)
        os.makedirs(download_path)
        download_zip_from_url(self.ANNOTATIONS_URL,download_path)
        return download_path

    def download_signals(self,extract_mono=True):
        if os.path.isdir(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        os.makedirs(self.temp_dir)
        stereo_temp_path = os.path.join(self.temp_dir, self.STEREO_AUDIO_DIR)
        mono_temp_path = os.path.join(self.temp_dir,self.MONO_AUDIO_DIR)
        stereo_output_path = os.path.join(self.download_dir,self.STEREO_AUDIO_DIR)
        mono_output_path = os.path.join(self.download_dir,self.MONO_AUDIO_DIR) if extract_mono else None
        os.makedirs(stereo_temp_path)
        os.makedirs(mono_temp_path)
        # Download each file individually.
        for audiofile in self.STEREO_AUDIO_FILENAMES:
            url = os.path.join(self.STEREO_AUDIO_URL,audiofile)
            download_from_url(url,"{}/{}".format(stereo_temp_path,audiofile))
            # Copy all the downloaded files from dir and move to output dir
        stereo_paths = glob.glob("{}/*".format(stereo_temp_path))
        if extract_mono:
            for stereo_path in stereo_paths:
                stereo_to_mono(stereo_path,mono_temp_path,
                                    left_prefix="g",right_prefix="f")
            shutil.move(mono_temp_path,mono_output_path)
        shutil.move(stereo_temp_path,stereo_output_path)
        shutil.rmtree(self.temp_dir)
        return stereo_output_path, mono_output_path


def test_download():
    """
    Pytest test for sample downloading -- only runs if script ran with pytest.
    """
    out_dir = "./maptask_test_download"
    os.makedirs(out_dir,exist_ok=True)
    loader = MapTaskDownloader(out_dir)
    path = loader.download_annotations()
    print(path)
    stereo_path, mono_path = loader.download_signals()
    print(stereo_path,mono_path)


