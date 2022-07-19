# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-19 14:30:32
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-19 16:46:16

import sys
import os
import re
from glob import glob

def get_utterances(transcription_root_dir,conversation):
    filepath = os.path.join(transcription_root_dir,f"{conversation}.cha")
    print("conversation", conversation)
    with open(filepath,'r') as f:
        # Cleaning up the data
        conv = f.readlines()
        for j in range(len(conv)):
            target_str = conv[j].strip()
            # Remove all comments

            split_toks = [re.split(r"\. |\?|\t+", target_str)]
            # Remove all punctuation and lowercase all
            split_toks = [re.sub(r'[^\w\s]', '', tok).lower() for tok in split_toks]
            print(split_toks)
        sys.exit(-1)