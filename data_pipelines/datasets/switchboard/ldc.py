# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-21 11:19:54
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-21 15:42:57


import os
import sys
import itertools
from turtle import right
from tqdm import tqdm
from collections import defaultdict

from data_pipelines.datasets.utils import sph2pipe


class LDCAudioCorpusReader:
    """
    Class to read / resolve file paths from the switchboard corpus audio obtained
    from the LDC. Generates stereo and mono wav files from the data.
    Link: https://catalog.ldc.upenn.edu/LDC97S62
    """

    # Mapping from audio channel to the participant.
    PARTICIPANTS = ("A", "B")
    CHANNEL_PARTICIPANT_MAPS = {
        1 : "A",
        2 : "B"
    }
    _DISKS = ("swb1_d1", "swb1_d2", "swb1_d3", "swb1_d4")

    def __init__(self, root_path):
        self.root_path = root_path
        assert os.path.isdir(root_path)
        self.sph_map = self.__generate_sph_map()
        self.wav_map = self.__generate_wav_map()
        self.mono_map = self.__generate_mono_map()

    @property
    def disks(self):
        return list(filter(lambda dir: os.path.isdir(dir) and \
                os.path.basename(dir) in self._DISKS,[os.path.join(self.root_path,d) \
            for d in os.listdir(self.root_path)]))

    @property
    def sph_paths(self):
        return self.sph_map

    @property
    def wav_paths(self):
        return self.wav_map

    @property
    def mono_paths(self):
        return self.mono_map

    def __generate_sph_map(self):
        path_map = {}
        for disk in self.disks:
            path = os.path.join(disk,'data')
            files = os.listdir(path)
            paths = [os.path.join(path,p) for p in files if p.endswith(".sph")]
            path_map.update({
                self.__extract_session(path) : path for path in paths
            })
        return path_map

    def __generate_wav_map(self):
        """Converts all files to wav if the wav does not already exist."""
        # Extract to a separate directory
        wav_dir = os.path.join(self.root_path,"LDC_data_wav")
        os.makedirs(wav_dir,exist_ok=True)
        wav_map = {}
        for sph_filepath in tqdm(self.sph_paths.values(),desc="Extracting wav"):
            session = self.__extract_session(sph_filepath)
            wav_map[session] = sph2pipe(sph_filepath,wav_dir)
        return wav_map

    def __generate_mono_map(self):
        """Extract the different speakers into different channels"""
        path_map = defaultdict(lambda : dict())
        mono_dir = os.path.join(self.root_path,"LDC_data_mono")
        os.makedirs(mono_dir,exist_ok=True)
        wav_paths = self.wav_paths.values()
        for path in tqdm(wav_paths,desc="Separating speaker channels"):
            session = self.__extract_session(path)
            # Generate the outputs
            for channel,speaker in self.CHANNEL_PARTICIPANT_MAPS.items():
                outfile = sph2pipe(
                    path,mono_dir,outfile_suffix=f".{speaker}",c=channel)
                path_map[session][speaker] = outfile
        return path_map

    def get_sessions(self):
        return sorted(list(set([self.__extract_session(p) \
            for p in self.sph_paths.values()])))

    def __extract_session(self, path):
        return os.path.splitext(os.path.basename(path))[0][3:]