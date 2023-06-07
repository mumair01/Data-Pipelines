# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-21 16:35:56
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-06-07 11:08:15


"""
Contains utilities for loading the callfriend corpus specifically. 
"""

import sys
import os
import re
import glob
from typing import Dict, List


# TODO: Need to clean up the data better.
def get_utterances(transcription_root_dir: str, conversation: str) -> Dict:
    """
    Obtain processed / cleaned utterances from the callfriend corpus.
    Preprocessing includes:
        - Replacing tabs and newlines.
        - Lowercasing all words.
        - Removing special characters.
    """
    filepath = os.path.join(transcription_root_dir, f"{conversation}.cha")
    with open(filepath, "r") as f:
        # --- Cleaning up the data
        conv = f.readlines()
        # Remove all comment lines - start with @
        conv = filter(lambda line: line[0] != "@", conv)
        # Remove any non-utterance lines - utterances always begin with * symbol.
        conv = filter(lambda line: line[0] == "*", conv)
        conv = list(conv)
        utterances = []
        for j in range(len(conv)):
            target_str = conv[j]
            # Separate the speaker tokens and text
            split_toks = re.split(":", target_str, 1)
            # Clean up special characters and lowercase all.
            split_toks = [
                re.sub(r"[^\w\s+]", "", tok).lower() for tok in split_toks
            ]
            # Replace tabs and newlines
            split_toks = [
                re.sub("\r?\n", "", tok).lower() for tok in split_toks
            ]
            split_toks = [re.sub(r"\t", "", tok).lower() for tok in split_toks]
            # At this point, we should have a speaker label and [text + times]
            if len(split_toks) == 2:
                times = re.findall(r"\d+", split_toks[1])
                if len(times) == 2:
                    start = float(times[0]) / 1000.0
                    end = float(times[1]) / 1000.0
                    text = re.sub(f"{times[0]}_{times[1]}", "", split_toks[1])
                else:
                    start = -1
                    end = -1
                    text = split_toks[1]
                utterances.append(
                    {
                        "speaker": split_toks[0],
                        "start": start,
                        "end": end,
                        "text": text,
                    }
                )
        return utterances


def get_audio_path(media_root_dir: str, conversation: str) -> str:
    """Obtain the path of the audio file corresponding to the given conversation"""
    path = "{}/{}.mp3".format(media_root_dir, conversation)
    return path


def get_conversations(transcription_root_dir: str) -> List[str]:
    """Obtain all the conversation chat file paths"""
    conversations = glob.glob("{}/*.cha".format(transcription_root_dir))
    # We only want the names of the conversation
    return [
        os.path.splitext(os.path.basename(conv))[0] for conv in conversations
    ]
