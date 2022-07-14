# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-12 15:54:44
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-13 09:30:28

##############################
# Utils for parsing the maptask corpus specifically
##############################

import os
import sys
import xml

################################# GLOBALS ####################################


# Paths within the maptask corpus
RELATIVE_TIMED_UNIT_PATHS = "Data/timed-units"
RELATIVE_POS_PATH = "Data/pos"

# Parts of speech tags present in the corpus.
POS_TAGS = [
    "vb",
    "vbd",
    "vbg",
    "vbn",
    "vbz",
    "nn",
    "nns",
    "np",
    "jj",
    "jjr",
    "jjt",
    "ql",
    "qldt",
    "qlp",
    "rb",
    "rbr",
    "wql",
    "wrb",
    "not",
    "to",
    "be",
    "bem",
    "ber",
    "bez",
    "do",
    "doz",
    "hv",
    "hvz",
    "md",
    "dpr",
    "at",
    "dt",
    "ppg",
    "wdt",
    "ap",
    "cd",
    "od",
    "gen",
    "ex",
    "pd",
    "wps",
    "wpo",
    "pps",
    "ppss",
    "ppo",
    "ppl",
    "ppg2\"",
    "pr",
    "pn",
    "in",
    "rp",
    "cc",
    "cs",
    "aff",
    "fp",
    "noi",
    "pau",
    "frag",
    "sent"
]


################################# GLOBALS ####################################


def get_maptask_file_participant(maptask_file_path):
    """Parse the participant from file path based on maptask naming convention"""
    return os.path.splitext(os.path.basename(maptask_file_path))[0].split(".")[1]

def get_maptask_file_dialogue(maptask_file_path):
    """Parse the dialogue from file path based on maptask naming convention"""
    return os.path.splitext(os.path.basename(maptask_file_path))[0].split(".")[0]

def get_maptask_file(dir_path, dialogue_name, participant, ext):
    """
    Get the path to a file with given participant and dialogue from a maptask
    directory that follows the maptask naming convention.
    """
    data_paths = [p for p in os.listdir(dir_path)]
    data_paths = [os.path.join(dir_path,p) for p in data_paths if os.path.splitext(p)[1][1:] == ext]
    for path in data_paths:
       if get_maptask_file_dialogue(path) == dialogue_name and \
                get_maptask_file_participant(path) == participant:
            return path

def get_utterance_times(maptask_root_path, dialogue, participant):
    """
    Obtain the start and end time for every utterance.
    Note that the utterance is defined as when there is any voice activity.
    The times are returned in seconds
    """
    timed_unit_dir = os.path.join(maptask_root_path,RELATIVE_TIMED_UNIT_PATHS)
    timed_unit_path = get_maptask_file(
        timed_unit_dir,dialogue,participant,"xml")[0]
    # Read the xml file
    tree = xml.etree.ElementTree.parse(timed_unit_path).getroot()
    # Extracting the audio end time from te timed units file.
    tu_tags = tree.findall('tu')
    va_times = []
    for tu_tag in tu_tags:
        start_time_s = float(tu_tag.get('start'))
        end_time_s = float(tu_tag.get('end'))
        va_times.append((start_time_s,end_time_s))
    return va_times


def get_utterance_pos_annotations(maptask_root_path, dialogue, participant):
    """
    Obtain the parts of speech annotations for all utterances where there
    is any voice activity.
    """
    timed_unit_dir = os.path.join(maptask_root_path,RELATIVE_TIMED_UNIT_PATHS)
    pos_dir = os.path.join(maptask_root_path,RELATIVE_POS_PATH)
    timed_unit_path = get_maptask_file(
        timed_unit_dir,dialogue,participant,"xml")[0]
    tree_timed_unit = xml.etree.ElementTree.parse(timed_unit_path).getroot()
    tu_tags = tree_timed_unit.findall("tu")
    pos_path = timed_unit_path = get_maptask_file(
        pos_dir,dialogue,participant,"xml")[0]
    tree_pos = xml.etree.ElementTree.parse(pos_path).getroot()
    # The pos is the tag attribute in all the tw tags.
    tw_tags = tree_pos.findall("tw")
    # Collecting the end time of the word and the corresponding POS tag.
    word_annotations = []
    for tu_tag in tu_tags:
        tu_tag_id = tu_tag.get("id")[7:]
        end_time_s = float(tu_tag.get('end'))
        for tw_tag in tw_tags:
            # NOTE: Not sure if this is the correct way to extract the corresponding
            # timed-unit id.
            href = list(tw_tag.iter())[1].get("href")
            _, href_ids = href.split("#")
            # Look at the appropriate file tags based on the filename.
            href_ids = href_ids.split("..")
            for href_id in href_ids:
                href_id = href_id[href_id.find("(")+8:href_id.rfind(")")]
                if href_id == tu_tag_id:
                    if tw_tag.get("tag") in POS_TAGS:
                        word_annotations.append((end_time_s,tw_tag.get("tag")))
    return word_annotations

