# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-12 15:54:44
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-19 11:51:58

"""
Utils for parsing the maptask corpus specifically
"""

import os
import sys
import xml
import glob
from typing import List, Dict, Tuple

from data_pipelines.datasets.maptask.constants import (
    POS_TAGS,
    RELATIVE_POS_DIR,
    RELATIVE_TIMED_UNITS_DIR,
)


def get_maptask_file_participant(maptask_file_path: str) -> str:
    """Parse the participant from file path based on maptask naming convention"""
    return os.path.splitext(os.path.basename(maptask_file_path))[0].split(".")[
        1
    ]


def get_maptask_file_dialogue(maptask_file_path: str) -> str:
    """Parse the dialogue from file path based on maptask naming convention"""
    return os.path.splitext(os.path.basename(maptask_file_path))[0].split(".")[
        0
    ]


def get_maptask_file(
    dir_path: str, dialogue_name: str, participant: str, ext: str
) -> str:
    """Get the path to a file with given participant and dialogue from a maptask
    directory that follows the maptask naming convention"""
    data_paths = [p for p in os.listdir(dir_path)]
    data_paths = [
        os.path.join(dir_path, p)
        for p in data_paths
        if os.path.splitext(p)[1][1:] == ext
    ]
    for path in data_paths:
        if (
            get_maptask_file_dialogue(path) == dialogue_name
            and get_maptask_file_participant(path) == participant
        ):
            return path
    raise Exception(
        (
            f"ERROR: Maptask dialogue {dialogue_name}, "
            f"participant: {participant} not found in {dir_path}"
        )
    )


def get_dialogues(maptask_root_path: str) -> List[str]:
    """Get the names of all the dialogues in the corpus"""
    timed_unit_dir = os.path.join(maptask_root_path, RELATIVE_TIMED_UNITS_DIR)
    assert os.path.isdir(timed_unit_dir)
    timed_unit_paths = glob.glob("{}/*.xml".format(timed_unit_dir))
    return set([get_maptask_file_dialogue(path) for path in timed_unit_paths])


def get_utterances(
    maptask_root_path: str, dialogue: str, participant: str
) -> List[Dict]:
    """Obtain the utterances in the corpus along with their start and end time"""
    timed_unit_dir = os.path.join(maptask_root_path, RELATIVE_TIMED_UNITS_DIR)
    timed_unit_path = get_maptask_file(
        timed_unit_dir, dialogue, participant, "xml"
    )
    # Read the xml file
    tree = xml.etree.ElementTree.parse(timed_unit_path).getroot()
    # Extracting the audio end time from te timed units file.
    tu_tags = tree.findall("tu")
    utterances = []
    for tu_tag in tu_tags:
        start_time_s = float(tu_tag.get("start"))
        end_time_s = float(tu_tag.get("end"))
        word = str(tu_tag.text)
        utterances.append(
            {"start": start_time_s, "end": end_time_s, "text": word}
        )
    return utterances


def get_utterance_pos_annotations(
    maptask_root_path: str, dialogue: str, participant: str
) -> Dict:
    """
    Obtain the parts of speech annotations for all utterances where there
    is any voice activity.
    Returns:
        (Dict: Map from utterance end time to part of speech tag
    """
    timed_unit_dir = os.path.join(maptask_root_path, RELATIVE_TIMED_UNITS_DIR)
    pos_dir = os.path.join(maptask_root_path, RELATIVE_POS_DIR)
    timed_unit_path = get_maptask_file(
        timed_unit_dir, dialogue, participant, "xml"
    )
    tree_timed_unit = xml.etree.ElementTree.parse(timed_unit_path).getroot()
    tu_tags = tree_timed_unit.findall("tu")
    pos_path = timed_unit_path = get_maptask_file(
        pos_dir, dialogue, participant, "xml"
    )
    tree_pos = xml.etree.ElementTree.parse(pos_path).getroot()
    # The pos is the tag attribute in all the tw tags.
    tw_tags = tree_pos.findall("tw")
    # Collecting the end time of the word and the corresponding POS tag.
    word_annotations = {}
    for tu_tag in tu_tags:
        tu_tag_id = tu_tag.get("id")[7:]
        end_time_s = float(tu_tag.get("end"))
        for tw_tag in tw_tags:
            # NOTE: Not sure if this is the correct way to extract the corresponding
            # timed-unit id.
            href = list(tw_tag.iter())[1].get("href")
            _, href_ids = href.split("#")
            # Look at the appropriate file tags based on the filename.
            href_ids = href_ids.split("..")
            for href_id in href_ids:
                href_id = href_id[href_id.find("(") + 8 : href_id.rfind(")")]
                if href_id == tu_tag_id:
                    if tw_tag.get("tag") in POS_TAGS:
                        word_annotations[end_time_s] = tw_tag.get("tag")
    return word_annotations
