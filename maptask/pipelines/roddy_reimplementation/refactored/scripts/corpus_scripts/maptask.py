# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-05-11 14:44:15
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-12 16:10:35
'''
This file contains contains a class that is able to download the maptask corpus
along with the audio and parse it as needed.
'''
import os
import subprocess
import sys
import glob
import shutil
from pathlib import Path
import re
import numpy as np
import h5py
# Locals
from utils import *


class MapTask:

    # ---- CONSTANTS
    ANNOTATIONS_URL = "http://groups.inf.ed.ac.uk/maptask/hcrcmaptask.nxtformatv2-1.zip"
    # Relative paths inside the expected corpus folder
    MAPTASK_DATA_DIR = "Data"
    MAPTASK_TIMED_UNITS_DIR = os.path.join(MAPTASK_DATA_DIR, "timed-units")
    MAPTASK_SIGNALS_PATH = os.path.join(MAPTASK_DATA_DIR, "signals")
    MAPTASK_STEREO_AUDIO_PATH = os.path.join(MAPTASK_SIGNALS_PATH, "dialogues")
    MAPTASK_MONO_AUDIO_PATH = os.path.join(
        MAPTASK_SIGNALS_PATH, "mono_dialogues")

    def __init__(self, load_dir, audio_wget_script_path, corpus_subset=1.0, seed=42):
        # Vars.
        self.corpus_path = None
        self.audio_wget_script = audio_wget_script_path
        self.load_dir = load_dir
        # Loading
        assert os.path.isfile(audio_wget_script_path)
        self.corpus_path = self.__load_corpus(load_dir)
        # Load all the important paths once
        self.subset_filenames = self.__get_subset_filenames(
            seed, corpus_subset)

    ############################# PUBLIC ###################################

    def get_stereo_audio_paths(self):
        paths = get_paths_from_directory(
            os.path.join(self.corpus_path, self.MAPTASK_STEREO_AUDIO_PATH))
        return [path for path in paths if ".mix.wav" in path
                and get_filename_from_path(path) in self.subset_filenames]

    # TODO: Need to add more than participant.

    def get_mono_audio_paths(self, participant=None):
        paths = get_paths_from_directory(
            os.path.join(self.corpus_path, self.MAPTASK_MONO_AUDIO_PATH))
        # extract only subset
        paths = [path for path in paths
                 if get_filename_from_path(path)[:5] in self.subset_filenames]
        if participant == None:
            # Collect the f and g files
            return paths
        if participant == 'f':
            return [p for p in paths if self.__get_file_participant(p) == 'f']
        if participant == 'g':
            return [p for p in paths if self.__get_file_participant(p) == 'g']

    # TODO: Need to add more than participant.
    def get_timed_units(self, participant=None):
        paths = get_paths_from_directory(
            os.path.join(self.corpus_path, self.MAPTASK_TIMED_UNITS_DIR))
        paths = [path for path in paths
                 if get_filename_from_path(path)[:5] in self.subset_filenames]
        if participant == None:
            return [path for path in paths if ".timed-units.xml" in path]
        elif participant == "f":
            return [path for path in paths if ".f.timed-units.xml" in path]
        elif participant == "g":
            return [path for path in paths if ".g.timed-units.xml" in path]

    def get_corpus_path(self):
        return self.corpus_path

    ############################# PRIVATE ###################################

    # ---- Download methods
    def __download_corpus(self, download_dir):
        if os.path.isdir(download_dir):
            shutil.rmtree(download_dir)
        os.makedirs(download_dir)
        corpus_path = self.__download_annotations(download_dir)
        self.__download_audio(corpus_path, self.audio_wget_script)
        self.__generate_mono_signals(corpus_path)
        return corpus_path

    def __download_annotations(self, download_dir):
        download_zip_from_url(self.ANNOTATIONS_URL, download_dir)
        return os.path.join(
            download_dir, os.listdir(download_dir)[0])

    def __download_audio(self, corpus_path, audio_wget_script_path):
        """
        Assumptions:
            1. The annotations are already downloaded.
        """
        assert os.path.isdir(corpus_path)
        assert os.path.isfile(audio_wget_script_path)
        signals_downloaded_path = os.path.join(os.getcwd(), "signals")
        # Make sure a dir called signals does not already exist.
        if os.path.isdir(signals_downloaded_path):
            shutil.rmtree(signals_downloaded_path)
        assert os.path.isdir(
            os.path.join(corpus_path, self.MAPTASK_DATA_DIR))
        os.makedirs(os.path.join(
            corpus_path, self.MAPTASK_SIGNALS_PATH), exist_ok=True)
        if not os.path.isdir(signals_downloaded_path):
            subprocess.run(
                "chmod +x {}".format(audio_wget_script_path), shell=True)
            subprocess.run(audio_wget_script_path, shell=True)
        assert os.path.isdir(signals_downloaded_path)
        shutil.move(signals_downloaded_path,
                    os.path.join(corpus_path, self.MAPTASK_SIGNALS_PATH))
        assert os.path.isdir(
            os.path.join(corpus_path, self.MAPTASK_STEREO_AUDIO_PATH))

    # ---- Loading methods

    def __load_corpus(self, load_dir):
        """
        Assumptions:
            1. Load dir should be the path to a directory containing the entire
            maptask directory.
        """
        if not os.path.isdir(load_dir):
            return self.__download_corpus(load_dir)
        assert os.path.isdir(load_dir)
        corpus_path = glob.glob("{}/maptask*".format(load_dir))
        if not len(corpus_path) == 1:
            return self.__download_corpus(load_dir)
        corpus_path = os.path.abspath(corpus_path[0])
        assert self.__verify_corpus_annotations(corpus_path)
        if not os.path.isdir(os.path.join(corpus_path, self.MAPTASK_STEREO_AUDIO_PATH)):
            self.__download_audio(corpus_path, self.audio_wget_script)
        if not os.path.isdir(os.path.join(corpus_path, self.MAPTASK_MONO_AUDIO_PATH)):
            self.__generate_mono_signals(corpus_path)
        self.__verify_corpus(corpus_path)
        return corpus_path

    # ---- Verification

    def __verify_corpus(self, corpus_path):
        return os.path.isdir(corpus_path) and \
            self.__verify_corpus_annotations(corpus_path) and \
            self.__verify_corpus_audio(corpus_path)

    def __verify_corpus_annotations(self, corpus_path):

        return os.path.isdir(os.path.join(corpus_path, self.MAPTASK_DATA_DIR)) and \
            os.path.isdir(os.path.join(
                corpus_path, self.MAPTASK_TIMED_UNITS_DIR))

    def __verify_corpus_audio(self, corpus_path):
        return os.path.isdir(os.path.join(corpus_path, self.MAPTASK_DATA_DIR)) and \
            os.path.isdir(os.path.join(
                corpus_path, self.MAPTASK_SIGNALS_PATH)) and \
            os.path.isdir(os.path.join(
                corpus_path, self.MAPTASK_STEREO_AUDIO_PATH)) and \
            os.path.isdir(os.path.join(
                corpus_path, self.MAPTASK_MONO_AUDIO_PATH))

    # ---- Audio

    def __generate_mono_signals(self, corpus_path):
        # TODO: Make sure the left signal is g and the right is f.
        stereo_dir = os.path.join(corpus_path, self.MAPTASK_STEREO_AUDIO_PATH)
        mono_dir = os.path.join(corpus_path, self.MAPTASK_MONO_AUDIO_PATH)
        os.makedirs(mono_dir)
        assert os.path.isdir(stereo_dir)
        # Convert all the stereo files into mono
        # NOTE: Audio ext. is wav for original data. See: https://groups.inf.ed.ac.uk/maptask/maptasknxt.html
        stereo_paths = glob.glob("{}/*mix.wav".format(stereo_dir))
        pbar = tqdm(
            total=len(stereo_paths), desc="Extracting mono from stereo")
        for stereo_path in stereo_paths:
            stereo_to_mono(stereo_path, mono_dir)
            pbar.update(1)

    # ---- Filenames

    def __get_file_quad(self, file_path):
        return get_filename_from_path(file_path)[:2]

    def __get_file_eye_contact(self, file_path):
        return get_filename_from_path(file_path)[2:4]

    def __get_file_dialogue(self, file_path):
        return get_filename_from_path(file_path)[4]

    def __get_file_participant(self, file_path):
        if ".f." in file_path:
            return 'f'
        if ".g." in file_path:
            return 'g'

    #  ---- Collection

    #  ---- Others

    def __get_subset_filenames(self, seed, corpus_subset):
        paths = get_paths_from_directory(
            os.path.join(self.corpus_path, self.MAPTASK_STEREO_AUDIO_PATH))
        filenames = [get_filename_from_path(p)[:5] for p in paths]
        subset_len = int((corpus_subset * len(filenames)))
        np.random.seed(seed)
        subset_filenames = np.random.choice(filenames, size=subset_len)
        return subset_filenames


def unittest():
    maptask = MapTask(
        load_dir="./dataset",
        audio_wget_script_path="/Users/muhammadumair/Documents/Repositories/mumair01-repos/Data-Pipelines/maptask/refactored/sh/maptaskBuild-12410-Mon-May-9-2022.wget.sh",
        corpus_subset=0.01
    )
    maptask.get_stereo_audio_paths()
    # print(maptask.get_mono_audio_paths(participant='g'))
    print(maptask.get_timed_units(participant='f'))
    # print(maptask.get_corpus_path())


if __name__ == "__main__":
    unittest()
