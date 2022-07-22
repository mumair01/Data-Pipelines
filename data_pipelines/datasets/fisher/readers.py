# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-22 12:13:39
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-22 13:52:16


import os
import sys
import itertools
from turtle import right
from tqdm import tqdm
import re
from collections import defaultdict


class LDCTranscriptsReader:

    def __init__(self, root_dir):
        assert os.path.isdir(root_dir)
        self.root_dir = root_dir
        self.map = self.__generate_map()


    def get_sessions(self):
        return list(self.map.keys())

    def get_session_transcript(self, session):
        with open(self.map[session]['trans'],'r') as f:
            utts = []
            conv = f.readlines()
            # Skip the comments and empty lines
            conv = [line for line in conv if not line.startswith("#")]
            # Clean newlines
            conv = [re.sub(r'\n','',line).strip() for line in conv]
            # Skipping empty lines
            conv = [line for line in conv if len(line) > 0]
            for line in conv:
                start, end, speaker, text = line.split(maxsplit=3)
                # Clean the parenthesis in the text
                text = re.sub(r'[^\(]*(\(.*\))[^\)]*','',text)
                utts.append({
                    "start" : float(start),
                    "end" : float(end),
                    "speaker" : speaker[:-1],
                    "text" : text
                 })
            return utts

    def __generate_map(self):
        """Parse the directory structure to produce a map with paths
        for each session."""
        map = defaultdict(lambda : dict())
        data_dir = os.path.join(self.root_dir,"data","trans")
        trans_subdirs =  list(filter(lambda dir: os.path.isdir(dir),
                [os.path.join(data_dir,d) for d in os.listdir(data_dir)]))
        trans_filepaths = [os.path.join(subdir,f) for subdir in trans_subdirs \
             for f in os.listdir(subdir)]
        for filepath in trans_filepaths:
            session = os.path.splitext(os.path.basename(filepath))[0]
            map[session]["trans"] = filepath
        return map

class LDCAudioReader:

    def __init__(self, root_dir):
        pass