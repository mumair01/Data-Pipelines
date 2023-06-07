# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-22 12:13:39
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-06-07 11:19:02


import os
import sys
import itertools
from turtle import right
from tqdm import tqdm
import re
import glob
from collections import defaultdict

from data_pipelines.datasets.utils import get_subdirs, sph2pipe
from typing import Dict, List

"""
Contains classes that are able to parse specific variants of the Fisher corpus. 
"""


class LDCTranscriptsReader:
    """
    Utility for parsing the LDC transcripts of the fisher corpus.
    Corpus link: https://catalog.ldc.upenn.edu/LDC2004T19
    """

    def __init__(self, root_dir: str):
        """
        Args:
            root_dir (str): Path to the root directory containing transcripts.
        """
        assert os.path.isdir(root_dir)
        self.root_dir = root_dir
        self.map = self.__generate_map()

    def get_sessions(self):
        """Obtain a list of session names in the corpus"""
        return list(self.map.keys())

    def get_session_transcript(self, session: str) -> List[Dict]:
        """Obtain the transcript of the specified session"""
        with open(self.map[session]["trans"], "r") as f:
            utts = []
            conv = f.readlines()
            # Skip the comments and empty lines
            conv = [line for line in conv if not line.startswith("#")]
            # Clean newlines
            conv = [re.sub(r"\n", "", line).strip() for line in conv]
            # Skipping empty lines
            conv = [line for line in conv if len(line) > 0]
            for line in conv:
                start, end, speaker, text = line.split(maxsplit=3)
                # Clean the parenthesis in the text
                text = re.sub(r"[^\(]*(\(.*\))[^\)]*", "", text)
                utts.append(
                    {
                        "start": float(start),
                        "end": float(end),
                        "speaker": speaker[:-1],
                        "text": text,
                    }
                )
            return utts

    def __generate_map(self):
        """Parse the directory structure to produce a map with paths
        for each session."""
        map = defaultdict(lambda: dict())
        data_dir = os.path.join(self.root_path, "data", "trans")
        trans_subdirs = list(
            filter(
                lambda dir: os.path.isdir(dir),
                [os.path.join(data_dir, d) for d in os.listdir(data_dir)],
            )
        )
        trans_filepaths = [
            os.path.join(subdir, f)
            for subdir in trans_subdirs
            for f in os.listdir(subdir)
        ]
        for filepath in trans_filepaths:
            session = os.path.splitext(os.path.basename(filepath))[0]
            map[session]["trans"] = filepath
        return map


class LDCAudioReader:
    """
    Utility for parsing the LDC Audio of the Fisher corpus.
    Corpus link:  https://catalog.ldc.upenn.edu/LDC2004S13

    """

    PARTICIPANTS = ("A", "B")
    # Mapping from audio channel to participants.
    CHANNEL_PARTICIPANT_MAPS = {1: "A", 2: "B"}

    def __init__(self, root_dir: str):
        """
        Args:
            root_dir (str): Path to the root directory containing transcripts.
        """
        assert os.path.isdir(root_dir)
        self.root_path = root_dir
        self.sph_map = self.__generate_sph_map()
        self.wav_map = self.__generate_wav_map()
        self.mono_map = self.__generate_mono_map()

    def get_sessions(self):
        """Obtain a list of session names in the corpus"""
        return list(self.sph_map.keys())

    def get_session_audio(self, session: str) -> Dict:
        """Obtain the audio paths of the given session"""
        return {
            "stereo": self.wav_map[session],
            "A": self.mono_map[session]["A"],
            "B": self.mono_map[session]["B"],
        }

    def __extract_session(self, path):
        return os.path.splitext(os.path.basename(path))[0].split("_")[-1]

    def __generate_sph_map(self):
        map = defaultdict(lambda: dict())
        disks = get_subdirs(self.root_path)
        for disk in disks:
            subdirs = get_subdirs(os.path.join(disk, "audio"))
            for dir in subdirs:
                files = glob.glob(f"{dir}/*.sph")
                map.update(
                    {self.__extract_session(file): file for file in files}
                )
        return map

    def __generate_wav_map(self):
        wav_dir = os.path.join(self.root_path, "LDC_data_wav")
        os.makedirs(wav_dir, exist_ok=True)
        wav_map = {}
        for sph_filepath in tqdm(self.sph_map.values(), desc="Extracting wav"):
            session = self.__extract_session(sph_filepath)
            wav_map[session] = sph2pipe(sph_filepath, wav_dir)
        return wav_map

    def __generate_mono_map(self):
        path_map = defaultdict(lambda: dict())
        mono_dir = os.path.join(self.root_path, "LDC_data_mono")
        os.makedirs(mono_dir, exist_ok=True)
        wav_paths = self.wav_map.values()
        for path in tqdm(wav_paths, desc="Separating speaker channels"):
            session = self.__extract_session(path)
            # Generate the outputs
            for channel, speaker in self.CHANNEL_PARTICIPANT_MAPS.items():
                outfile = sph2pipe(
                    path, mono_dir, outfile_suffix=f".{speaker}", c=channel
                )
                path_map[session][speaker] = outfile
        return path_map
