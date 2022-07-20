# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-20 13:57:04
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-20 19:18:51

"""
Utils / parsers for the  isip aligned switchboard transcripts
HOMEPAGE = https://isip.piconepress.com/projects/switchboard/
Keywords: Manually corrected work alignments
"""

import os
import sys
import itertools
import glob
import re

class ISIPAlignedCorpusReader:

    _TRANSCRIPTIONS_DIR = "swb_ms98_transcriptions"
    _VOCAB_FILENAME = "sw-ms98-dict.text"
    _LEVELS = ("trans", "word")
    PARTICIPANTS = ("A", "B")

    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.transcriptions_dir = os.path.join(
            root_dir,self._TRANSCRIPTIONS_DIR)
        self.__generate_sessions_map()

    def get_sessions(self):
        return list(self.sessions_map.keys())

    def get_session_transcript(self, session, participant):
        """
        Obtain a transcript of the session with the given participant at either the
        word or the turn level.
        """
        assert participant in self.PARTICIPANTS, \
            f"Participant must be one of {self.PARTICIPANTS}"
        # Read both the trans and word level data and merge
        trans_level, word_level = [self.__read_transcript(
            session,participant,level) for level in self._LEVELS]
        # Processed data includes the utterance and the associated words
        for item in trans_level:
            item.update({
                "tokens" : self.__words_in_range(
                                    word_level,item['start'],item['end'])
            })
        return trans_level

    def get_vocabulary(self):
        """Return a vocabulary of all the words in the corpus"""
        vocab_path = os.path.join(self.transcriptions_dir,self._VOCAB_FILENAME)
        words = []
        with open(vocab_path,'r') as f:
            lines = f.readlines()
            # Filter out the comments
            lines = [line for line in lines[1:] if line[0] != '#']
            for line in lines:
                words.extend(line.split())
            return list(set(words))

    # TODO: This is slow - figure out a way to make it faster.
    def __words_in_range(self, word_level, start, end):
        words = []
        for item in word_level:
            if item['start']  >= start and item['end'] <= end:
                words.append(item)
        return words


    def __generate_sessions_map(self):
        subdirs = glob.glob("{}/[!.]*/".format(self.transcriptions_dir))
        self.sessions_map = {}
        for subdir in subdirs:
            sessions = [f for f in  os.listdir(subdir) if not f.startswith(".")]
            self.sessions_map.update({
                session : os.path.join(self.transcriptions_dir,subdir,session) \
                    for session in sessions
            })

    def __read_transcript(self, session, participant,level):
        filepath = self.__get_transcript_path(session,participant,level)
        utts = []
        with open(filepath,'r') as f:
            lines = f.readlines()
            for line in lines:
                if '\t' in line:
                    data = line.split("\t")
                else:
                    data = line.split(' ')
                data = [d for d in data if len(d) > 0]
                start = float(data[1])
                end = float(data[2])
                text = re.sub('\n', ''," ".join(data[3:])).strip().lower()
                utts.append({
                    "start" : float(start),
                    "end" : float(end),
                    "text" : text
                })
        return sorted(utts, key=lambda utt: utt['start'])

    def __get_transcript_path(self,session, participant,level):
        sessions_dir = self.sessions_map[session]
        files = os.listdir(sessions_dir)
        for file in files:
            if self.__get_transcript_participant(file) == participant and \
                    self.__get_transcript_level(file) == level:
                return os.path.join(sessions_dir,file)

    def __get_transcript_participant(self, filepath):
        return filepath[6]

    def __get_transcript_session(self, filepath):
        return filepath[2:6]

    def __get_transcript_level(self, filepath):
        return filepath.split('.')[0].split('-')[-1]



