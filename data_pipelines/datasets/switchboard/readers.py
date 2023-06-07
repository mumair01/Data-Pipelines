# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-26 14:24:16
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-06-07 11:28:06

import os
import sys
import itertools
from turtle import right
from tqdm import tqdm
from collections import defaultdict
import glob
import re

from data_pipelines.datasets.utils import sph2pipe


"""
Contains classes that are able to parse specific variants of the Switchboard corpus. 
"""


class LDCAudioCorpusReader:
    """
    Class to read / resolve file paths from the switchboard corpus audio obtained
    from the LDC. Generates stereo and mono wav files from the data.
    Link: https://catalog.ldc.upenn.edu/LDC97S62
    """

    # Mapping from audio channel to the participant.
    PARTICIPANTS = ("A", "B")
    CHANNEL_PARTICIPANT_MAPS = {1: "A", 2: "B"}
    _DISKS = ("swb1_d1", "swb1_d2", "swb1_d3", "swb1_d4")

    def __init__(self, root_path):
        self.root_path = root_path
        assert os.path.isdir(root_path)
        self.sph_map = self.__generate_sph_map()
        self.wav_map = self.__generate_wav_map()
        self.mono_map = self.__generate_mono_map()

    @property
    def disks(self):
        return list(
            filter(
                lambda dir: os.path.isdir(dir)
                and os.path.basename(dir) in self._DISKS,
                [
                    os.path.join(self.root_path, d)
                    for d in os.listdir(self.root_path)
                ],
            )
        )

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
            path = os.path.join(disk, "data")
            files = os.listdir(path)
            paths = [os.path.join(path, p) for p in files if p.endswith(".sph")]
            path_map.update(
                {self.__extract_session(path): path for path in paths}
            )
        return path_map

    def __generate_wav_map(self):
        """Converts all files to wav if the wav does not already exist."""
        # Extract to a separate directory
        wav_dir = os.path.join(self.root_path, "LDC_data_wav")
        os.makedirs(wav_dir, exist_ok=True)
        wav_map = {}
        for sph_filepath in tqdm(
            self.sph_paths.values(), desc="Extracting wav"
        ):
            session = self.__extract_session(sph_filepath)
            wav_map[session] = sph2pipe(sph_filepath, wav_dir)
        return wav_map

    def __generate_mono_map(self):
        """Extract the different speakers into different channels"""
        path_map = defaultdict(lambda: dict())
        mono_dir = os.path.join(self.root_path, "LDC_data_mono")
        os.makedirs(mono_dir, exist_ok=True)
        wav_paths = self.wav_paths.values()
        for path in tqdm(wav_paths, desc="Separating speaker channels"):
            session = self.__extract_session(path)
            # Generate the outputs
            for channel, speaker in self.CHANNEL_PARTICIPANT_MAPS.items():
                outfile = sph2pipe(
                    path, mono_dir, outfile_suffix=f".{speaker}", c=channel
                )
                path_map[session][speaker] = outfile
        return path_map

    def get_sessions(self):
        return sorted(
            list(
                set(
                    [self.__extract_session(p) for p in self.sph_paths.values()]
                )
            )
        )

    def __extract_session(self, path):
        return os.path.splitext(os.path.basename(path))[0][3:]


class ISIPAlignedCorpusReader:
    """
    Utility class to read the ISIP aligned switchboard corpus, which are the
    same as the MSU transcripts.
    Link: https://isip.piconepress.com/projects/switchboard/
    """

    _TRANSCRIPTIONS_DIR = "swb_ms98_transcriptions"
    _VOCAB_FILENAME = "sw-ms98-dict.text"
    _LEVELS = ("trans", "word")
    PARTICIPANTS = ("A", "B")

    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.transcriptions_dir = os.path.join(
            root_dir, self._TRANSCRIPTIONS_DIR
        )
        self.__generate_sessions_map()

    def get_sessions(self):
        return list(self.sessions_map.keys())

    def get_session_transcript(self, session, participant):
        """
        Obtain a transcript of the session with the given participant at either the
        word or the turn level.
        """
        assert (
            participant in self.PARTICIPANTS
        ), f"Participant must be one of {self.PARTICIPANTS}"
        # Read both the trans and word level data and merge
        trans_level, word_level = [
            self.__read_transcript(session, participant, level)
            for level in self._LEVELS
        ]
        # Processed data includes the utterance and the associated words
        for item in trans_level:
            item.update(
                {
                    "tokens": self.__words_in_range(
                        word_level, item["start"], item["end"]
                    )
                }
            )
        return trans_level

    def get_vocabulary(self):
        """Return a vocabulary of all the words in the corpus"""
        vocab_path = os.path.join(self.transcriptions_dir, self._VOCAB_FILENAME)
        words = []
        with open(vocab_path, "r") as f:
            lines = f.readlines()
            # Filter out the comments
            lines = [line for line in lines[1:] if line[0] != "#"]
            for line in lines:
                words.extend(line.split())
            return list(set(words))

    # TODO: This is slow - figure out a way to make it faster.
    def __words_in_range(self, word_level, start, end):
        words = []
        for item in word_level:
            if item["start"] >= start and item["end"] <= end:
                words.append(item)
        return words

    def __generate_sessions_map(self):
        subdirs = glob.glob("{}/[!.]*/".format(self.transcriptions_dir))
        self.sessions_map = {}
        for subdir in subdirs:
            sessions = [f for f in os.listdir(subdir) if not f.startswith(".")]
            self.sessions_map.update(
                {
                    session: os.path.join(
                        self.transcriptions_dir, subdir, session
                    )
                    for session in sessions
                }
            )

    def __read_transcript(self, session, participant, level):
        filepath = self.__get_transcript_path(session, participant, level)
        utts = []
        with open(filepath, "r") as f:
            lines = f.readlines()
            for line in lines:
                if "\t" in line:
                    data = line.split("\t")
                else:
                    data = line.split(" ")
                data = [d for d in data if len(d) > 0]
                start = float(data[1])
                end = float(data[2])
                text = re.sub("\n", "", " ".join(data[3:])).strip().lower()
                utts.append(
                    {"start": float(start), "end": float(end), "text": text}
                )
        return sorted(utts, key=lambda utt: utt["start"])

    def __get_transcript_path(self, session, participant, level):
        sessions_dir = self.sessions_map[session]
        files = os.listdir(sessions_dir)
        for file in files:
            if (
                self.__get_transcript_participant(file) == participant
                and self.__get_transcript_level(file) == level
            ):
                return os.path.join(sessions_dir, file)

    def __get_transcript_participant(self, filepath):
        return filepath[6]

    def __get_transcript_session(self, filepath):
        return filepath[2:6]

    def __get_transcript_level(self, filepath):
        return filepath.split(".")[0].split("-")[-1]
