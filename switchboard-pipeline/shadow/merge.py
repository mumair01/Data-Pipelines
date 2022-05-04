# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-03-04 18:28:17
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-03-23 12:44:21

import os
import sys
import re
import csv
from typing import List, Dict
import tensorflow_datasets as tfds
from collections import defaultdict
from tqdm import tqdm
from utils import *
from dataclasses import dataclass

# -- MSU SPECIFIC


def get_msu_file_conv_number(file_path):
    filename = os.path.basename(file_path)
    return filename[2:6]


def get_msu_file_participant(file_path):
    filename = os.path.basename(file_path)
    return filename[6]


def get_msu_file_type(file_path):
    filename = os.path.basename(file_path)
    return filename[filename.rfind(".") - 4: filename.rfind(".")]


def parse_msu_timing_file(msu_timing_path):

    def process_line(line):
        conv_id, start, end, word = line.split()
        word = word.lower()
        if not (word[0] == "[" and word[-1] == "]"):
            if word[-1] != "-":
                word = re.sub('-', ' ', word)
            return {
                "conv_id": conv_id,
                "start": start,
                "end": end,
                "word": word}
    with open(msu_timing_path, 'r', encoding="UTF-8") as f:
        lines = f.readlines()
        print(msu_timing_path)
        lines = [process_line(line) for line in lines]
        lines = [line for line in lines if line != None]
        return lines

# -- LC SPECIFIC


def get_lc_file_collection_no(file_path):
    filename = os.path.basename(file_path)


def get_lc_file_no_in_collection(file_path):
    filename = os.path.basename(file_path)


def get_lc_file_conv_id(file_path):
    filename = os.path.basename(file_path)
    return filename[filename.rfind(".") - 4: filename.rfind(".")]


def parse_lc_dialogue_act_file(file_path, speaker):

    def process_line(line):
        try:
            line = line.strip().split()
            speech_act, speaker, utt_num, tcu_num = \
                line[0], line[1].split('.')[0], line[1].split('.')[1],\
                line[2][3:-1]
            words = []
            for word in line[3:]:
                if word[-1] != "-":
                    # We will match abandoned words
                    word = re.sub('-', ' ', word)
                word = re.sub(
                    '--|#|{[A-Z]|<[a-z]*\>|[(),+/?.{}\[\]]', '', word)
                if word.strip() != "":
                    words.append(word.lower())
            return {"speech_act": speech_act,
                    "speaker": speaker,
                    "utt_num": utt_num,
                    "tcu_num": tcu_num,
                    "words": words}
        except:
            pass

    acts = []
    with open(file_path, 'r', encoding="UTF-8") as f:
        lines = f.readlines()
        for line in lines:
            if f"{speaker}." in line:
                acts.append(process_line(line))
        return [act for act in acts if act != None]

# -- Merge utils


def find_file_matches(lc_dir_path, msu_dir_path):
    # Map from conv. no. to msu lc file tuples
    conv_no_to_matches = defaultdict(list)
    # Loading the lc files
    lc_utt_da_file_paths = get_files_with_ext(lc_dir_path, ".utt")
    # Loading the msu files
    msu_time_file_paths = get_files_with_ext(msu_dir_path, "word.text")
    for msu_time_path in msu_time_file_paths:
        conv_no = get_msu_file_conv_number(msu_time_path)
        for lc_utt_da_path in lc_utt_da_file_paths:
            if conv_no == get_lc_file_conv_id(lc_utt_da_path):
                conv_no_to_matches[conv_no].append(
                    (msu_time_path, lc_utt_da_path))
    return conv_no_to_matches


def merge_da_timing_data(dialogue_acts, timing, speaker):

    def parse_da_dictionary(dialogue_acts, index):
        utt_num = 0
        while index >= 0 and utt_num < len(dialogue_acts):
            num_words = len(dialogue_acts[utt_num]["words"])
            if index < num_words:
                return (dialogue_acts[utt_num]["words"][index],
                        utt_num,
                        dialogue_acts[utt_num]["speech_act"])
            index -= num_words
            utt_num += 1
        return (None, None, None)

    def parse_timing_dictionary(timing, index):
        if index < len(timing):
            return timing[index]["word"], timing[index]["start"],\
                timing[index]["end"]
        return (None, None, None)

    def obtain_parsed_data_in_range(start_index, end_index, data, source):
        """
        This is inclusive of both indices
        """
        result = list()
        for i in range(start_index, end_index + 1):
            if source == "timing":
                result.append(
                    parse_timing_dictionary(data, i))
            elif source == "da":
                result.append(parse_da_dictionary(data, i))
            else:
                raise Exception("Invalid source")
        return result

    def create_utterance(speaker, start, end, words, speech_act):
        return {
            "speaker": speaker, "start": start, "end": end,
            "words": " ".join(words), "speech_act": speech_act}

    timing_ptr = 0
    da_ptr = 0
    merged_utterances = []
    stored_data = {
        "words": [],
        "start": None,
        "end": None,
        "act": None,
        "utterance": None
    }
    prev_dialogue_act_word = None
    prev_timing_word = None

    while True:
        import sys
        if timing_ptr >= len(timing):
            break
        # Obtain the values at the current indices
        parsed_da_curr, parsed_da_next = \
            obtain_parsed_data_in_range(da_ptr, da_ptr+1, dialogue_acts, "da")
        parsed_timing_curr, parsed_timing_next = \
            obtain_parsed_data_in_range(
                timing_ptr, timing_ptr+1, timing, "timing")
        # Unpack the data
        da_word_curr, utt_curr, act_curr = parsed_da_curr
        da_word_next, utt_next, act_next = parsed_da_next
        timing_word_curr, timing_start_curr, timing_end_curr = parsed_timing_curr
        timing_word_next, timing_start_next, timing_end_next = parsed_timing_next
        # NOTE: There are eight cases that were originally defined.
        # Case 1: Words match
        if da_word_curr == timing_word_curr:
            print("case 1")
            if utt_curr != stored_data["utterance"] and len(stored_data["words"]) > 0:
                utterance = create_utterance(
                    speaker, stored_data["start"], stored_data["end"],
                    stored_data["words"], stored_data["act"])
                merged_utterances.append(utterance)
                stored_data.update({
                    "start": timing_start_curr,
                    "words": []})
            stored_data.update({
                "end": timing_end_curr,
                "act": act_curr,
                "utterance": utt_curr})
            stored_data["words"].append(timing_word_curr)
            timing_ptr += 1
            da_ptr += 1
        # Case 2: Timing has missing word
        elif da_word_curr == timing_word_next:
            print("case 2")
            if utt_next != stored_data["utterance"]:
                utterance = create_utterance(
                    speaker, stored_data["start"], stored_data["end"],
                    stored_data["words"], stored_data["act"])
                merged_utterances.append(utterance)
                stored_data.update({
                    "start": timing_start_curr,
                    "words": []})
            stored_data.update({
                "end": timing_end_curr,
                "act": act_curr,
                "utterance": utt_curr})
            stored_data["words"].extend([timing_word_curr, timing_word_next])
            timing_ptr += 2
            da_ptr += 1
        # Case 3: Dialogue Act has missing word
        elif da_word_next == timing_word_curr:
            print("case 3")
            if utt_next != stored_data["utterance"]:
                if stored_data["act"] != None:
                    utterance = create_utterance(
                        speaker, stored_data["start"], stored_data["end"],
                        stored_data["words"], stored_data["act"])
                    merged_utterances.append(utterance)
                stored_data.update({
                    "start": timing_start_curr,
                    "words": []})
            stored_data.update({
                "end": timing_end_curr,
                "act": act_next,
                "utterance": utt_next})
            stored_data["words"].append(timing_word_curr)
            timing_ptr += 1
            da_ptr += 2
        # Case 4: Timing word is abandoned,
            #  but matches dialogue act word start letter
        elif da_word_curr and "-" in timing_word_curr and \
                timing_word_curr[0] == da_word_curr[0]:
            print("case 4")
            if utt_next != stored_data["utterance"]:
                utterance = create_utterance(
                    speaker, stored_data["start"], stored_data["end"],
                    stored_data["words"], stored_data["act"])
                merged_utterances.append(utterance)
                stored_data.update({
                    "start": timing_start_curr,
                    "words": []})
            stored_data.update({
                "end": timing_end_curr,
                "act": act_curr,
                "utterance": utt_curr})
            stored_data["words"].append(timing_word_curr)
            timing_ptr += 1
            da_ptr += 1
        # Case 5: alternative transcription
        elif timing_word_curr and da_word_curr and \
                len(timing_word_curr) == len(da_word_curr) and \
                timing_word_curr[0] == da_word_curr[0]:
            print("case 5")
            if utt_next != stored_data["utterance"]:
                utterance = create_utterance(
                    speaker, stored_data["start"], stored_data["end"],
                    stored_data["words"], stored_data["act"])
                merged_utterances.append(utterance)
                stored_data.update({
                    "start": timing_start_curr,
                    "words": []})
            stored_data.update({
                "end": timing_end_curr,
                "act": act_curr,
                "utterance": utt_curr})
            stored_data["words"].append(timing_word_curr)
            timing_ptr += 1
            da_ptr += 1
        # Case 6: Dialogue act word repeat
        elif da_word_curr and \
                prev_dialogue_act_word == da_word_curr:
            print("case 6")
            stored_data.update({
                "act": act_curr,
                "utterance": utt_curr})
            da_ptr += 1
         # Case 7: Timing word repeat
        elif timing_word_curr and \
                prev_timing_word == timing_word_curr:
            print("case 7")
            stored_data.update({
                "end": timing_end_curr})
            stored_data["words"].append(timing_word_curr)
            timing_ptr += 1
        # Case 8: Default
        else:
            print("case 8")
            stored_data["words"].append(timing_word_curr)
            if stored_data["start"] == None:
                stored_data["start"] = timing_start_curr
            stored_data["end"] = timing_end_curr
            timing_ptr += 1

        prev_timing_word = timing_word_curr
        prev_dialogue_act_word = da_word_curr
    return merged_utterances


def output_as_csv(result_dir_path, conversation_id, utterances):
    if len(utterances) == 0:
        return
    columns = list(utterances[0].keys())
    result_file_path = os.path.join(
        result_dir_path, "{}.csv".format(conversation_id))
    os.makedirs(result_dir_path, exist_ok=True)
    with open(result_file_path, 'w') as f:
        write = csv.writer(f)
        write.writerow(columns)
        for utt in utterances:
            write.writerow(list(utt.values()))
    print("written to file: {}".format(result_file_path))


def merge_msu_lc_files(conv_no_to_matches, result_dir_path):

    for conv_no, matches in conv_no_to_matches.items():
        # Each conv matches should have two matches: one for speaker A and
        # one for speaker B.
        if len(matches) != 2:
            continue
        # Two timing files and two DA files, one per speaker.
        msu_time_path_A = matches[0][0] if  \
            get_msu_file_participant(matches[0][0]) == "A" else matches[1][0]
        msu_time_path_B = matches[0][0] if  \
            get_msu_file_participant(matches[0][0]) == "B" else matches[1][0]
        lc_utt_da_path = matches[0][1]
        # Generating the dialogue act files for speaker A and B.
        da_speaker_A = parse_lc_dialogue_act_file(lc_utt_da_path, "A")
        da_speaker_B = parse_lc_dialogue_act_file(lc_utt_da_path, "B")
        # obtain the timing information for both speakers
        timing_info_A = parse_msu_timing_file(msu_time_path_A)
        timing_info_B = parse_msu_timing_file(msu_time_path_B)
        # Merge all cases
        match_da_A_timing_A = merge_da_timing_data(
            da_speaker_A, timing_info_A, "A")
        match_da_B_timing_B = merge_da_timing_data(
            da_speaker_B, timing_info_B, "B")
        # match_da_B_timing_A = merge_da_timing_data(
        #     da_speaker_B, timing_info_A, "A")
        # match_da_A_timing_B = merge_da_timing_data(
        #     da_speaker_A, timing_info_B, "B")

        # TODO: This exact files to merge should be based on the error.
        matched_utterances = match_da_A_timing_A + match_da_B_timing_B
        # Sort the matched utterances
        matched_utterances = list(
            filter(lambda x: x["start"] is not None,  matched_utterances))
        matched_utterances.sort(key=lambda x: float(x["start"]))
        # Output all the files as csv.
        for item in matched_utterances:
            print(item)

        output_as_csv(result_dir_path, conv_no, matched_utterances)


def merge_msu_lc_sb_corpora(lc_dir_path, msu_dir_path, result_dir_path):
    conv_no_to_matches = find_file_matches(lc_dir_path, msu_dir_path)
    merge_msu_lc_files(conv_no_to_matches, result_dir_path)


'''

NOTE: MSU is the timing file and LLC is the dialogue act file.

Case 1: Words match

Case 2: Timing has missing word

# Case 3: Dialogue Act has missing word

# Case 4: Timing word is abandoned,
                #  but matches dialogue act word start letter

# Case 5: alternative transcription

# Case 6: Dialogue act word repeat

# Case 7: Timing word repeat

# Case 8: Default
'''
