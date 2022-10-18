"""
switchboard.py
"""
# Libraries and setup
import pandas as pd
import numpy as np
import re
from typing import List, Tuple
import difflib
# from tqdm import tqdm


import sys
import os
import glob

from enum import Enum
from Levenshtein import distance as lev

class Correction(Enum):
    EXACT_WORD_MATCH = 0
    REPEATED_OR_DELETED_WORD = 1
    ALTERNATIVE_TRANSCRIPTION = 2
    OTHER = 3 

# assumes the word array is more correct and may be longer than the utt array
# def correct_differences(word_arr: List, utt_arr: List, fallback = None) -> Tuple[List, Correction]:
#     word_len = len(word_arr)
#     utt_len = len(utt_arr)
#     word_diff_list = list(set(word_arr) - set(utt_arr))

#     # there are more/different words in the word list than there are in the utt list
#     if word_diff_list != []:
#         # case 1: if the word list has an extra turn in it, and the beginnings are an exact word match
#         # it means that the numbering in the ms98-a-word file was 
#         if word_arr[:utt_len] == utt_arr:
#             # TODO insert new row in speaker_word pandas df with fallback
#             return (utt_arr, Correction.EXACT_WORD_MATCH)

#         # case 2: check if the lists have a transcription error
#         else:
#             for diff in word_diff_list:
#                 diff_i = word_arr.index(diff) # the index where the diff is found in the original array
#                 diff_dist = lev(diff, utt_arr[diff_i])

#                 # if the levenstein distance between the target words is small, try running this recursively with 
#                 if diff_dist <= 3:
#                     utt_arr = utt_arr[:diff_i - 1] + [diff] + utt_arr[diff_i + 1:]
            
#             # if all else fails, just use the word array
#             return (word_arr, Correction.ALTERNATIVE_TRANSCRIPTION)

#     # no differences in the content of the word arrays
#     elif word_len != utt_len:
#         return (word_arr, Correction.REPEATED_OR_DELETED_WORD)
#     else:
#         return (word_arr, Correction.EXACT_WORD_MATCH)

# we want to minimize this
def char_error(word_arr: List[str], utt_arr: List[str]) -> int:
    # word_len = len(word_arr)
    # utt_len = len(utt_arr)

    word_set = set(word_arr)
    utt_set = set(utt_arr)
    word_diff_list = list(word_set - utt_set)

    # there may be repetitions or deletions
    if word_diff_list == []:
        return 0
    else:
        # str_diff = "".join(word_diff_list)

        utt_str = "".join(list(utt_set))
        word_str = "".join(list(word_set))

        lev_set_difference = lev(utt_str, word_str)
        return lev_set_difference

# assumes that each candidate list is successively longer than the last
def minimize_char_error(candidate_word_arrs: List[List[str]],
                        utt_arr: List[str],
                        next_turn_is_same = False) -> List[str]:
    best_error = np.inf # defaults to every character is wrong
    curr_candidate = []
    has_increased = False

    for word_arr in candidate_word_arrs:
        curr_error = char_error(word_arr, utt_arr)

        ######
        # print(f"char_error {curr_error} from {word_arr}")
        ######
        if curr_error <= best_error and (curr_candidate == [] or not(next_turn_is_same)):
            best_error = curr_error
            curr_candidate = word_arr
        elif (has_increased == True) or (best_error == 0):
            break # does not expand the search space when the 
        else:
            has_increased = True
    
    ######
    # print("candidate", curr_candidate)
    ######
    return curr_candidate
    
# TODO proper download
directory = "Transcript_Example/"
n_transcript = 3097
utt_path = directory + "1_sw_0614_" + str(n_transcript) + ".utt" # todo deal with reutterizing
word_A_path = directory + "0_sw" + str(n_transcript)  + "A-ms98-a-word.text"
word_B_path = directory + "0_sw" + str(n_transcript)  + "B-ms98-a-word.text"

"""
contains speaker: str, words: List[str],
    damsl: str, swbd_damsl: str
with empty cols for start, end, declarative,
    interrogative, imperative, non-syntactic,
    function:
"""
# def re_utterize(utt_path: str) -> pd.DataFrame:
#     utt_df = pd.data_frame()
#     speaker_A_num_utt = 0
#     speaker_B_num_utt = 0
#     with open(utt_path, "r", encoding="UTF-8") as utt_file:
#         print(f"we have {utt_path}")

#     # may be useful for debugging to have output options
#     # as pd.Dataframe or linguistic consortium file
#     return utt_df


"""
contains speaker,words,start,end, damsl,swbd_damsl,function information
with open cols for declarative,interrogative,imperative,non-syntactic,
"""
def merge(utt_path: str, word_A_path: str, word_B_path: str) -> None:
    a_df = pd.read_csv(word_A_path, sep=" ",
                names=["tcu_num", "start", "end", "words"])
    b_df = pd.read_csv(word_B_path, sep=" ",
                names=["tcu_num", "start", "end", "words"])
    

    # reads utterance file into dataframe
    # possible more elegant solutions
    # df_utt = pd.read_fwf(utt_path, sep=" ", skiprows=31, header=0,
    #         names=["damsl_function", "speaker", "num_continue", "words"])
    # df_utt = pd.read_csv(utt_path, skiprows=32)
    # utt_arr = np.loadtxt(utt_path, skiprows=32, dtype=str, delimiter=None)
    df_utt = pd.DataFrame()
    with open(utt_path, "r") as utt_file:
        utt_file = utt_file.readlines()[31:]
        for line in utt_file:
            # sanitizes files, based on chas' code
            def process_line(line):
                tokens = [word for word in line.strip().split()]
                speech_act = tokens[0]
                speaker = tokens[1][0] # assumes speaker is a single character letter
                turn_num = tokens[1][2:]
                utt_num = tokens[2][3:-1]
                words = []
                for word in tokens[3:]:
                    if word[-1] != "-":
                        # We will match abandoned words
                        # replace is faster than re on string literals
                        word = word.replace('-', ' ').replace('--', '').replace('#', '')
                        word = re.sub('{[A-Z]', '', word)
                        word = re.sub('<[a-z]*\>', '', word)
                        word = re.sub('[(),+/?.{}\[\]]', '', word)
                    if not word.strip() == "":
                        words.append(word.lower())

                return {"speech_act": speech_act,
                        "speaker": speaker,
                        "utt_num": utt_num,
                        "tcu_num": turn_num,
                        "words": words}

            new_row = process_line(line)
            df_utt = df_utt.append(new_row, ignore_index = True)
    
    utt_a_df, tcu_b_df = [x for _, x in df_utt.groupby(df_utt["speaker"] == "B")]
    
    # looks only at the speaker A timings
    a_df = a_df[a_df.words != "[silence]"]
    a_df = a_df[a_df.words != "[noise]"]
    a_df = a_df[a_df.words != "[laughter]"]
    a_df["words"] = a_df["words"].str.lower().str.replace('-', ' ') \
                        .str.replace('--', '').str.replace('#', '')
    word_a_df = a_df.groupby(['tcu_num'])['words'].apply(list).reset_index()


    

    word_arr = a_df["words"].values
    utt_arr = utt_a_df["words"].values
    # print(word_arr)

    # this is n^2, I know...
     
    for i in range(len(utt_arr)):
        utt = utt_arr[i]
        # testing sanity check
        if i > 15:
            break

        candidate = [word_arr[:i] for i in range(1, len(word_arr) + 1)]
        corrected = minimize_char_error(candidate, utt, utt_arr[i+1] == utt)

        #####
        print("curr utt", utt) # "next utt", utt_arr[i+1]
        # print("next turn is same?", np.array_equal(utt_arr[i+1], utt))
        print("turn result is", corrected)
        print("")
        #####

        # queues words that may be used in current word array
        new_word_arr = []
        num_corrected = 0
        for j in range(len(word_arr)):
            word = word_arr[j]
            if (num_corrected >= len(corrected)):
                new_word_arr = np.concatenate((new_word_arr, word_arr[j:]))
                break

            if word in corrected:
                num_corrected += 1
            else:
                new_word_arr.append(word)
        word_arr = new_word_arr

    	

       

        

    # transforms words dataframe such that each row has the smallest levenstein distance to the utterance dataframe

    # compares each turn 
    # print(word_a_df["words"][0])
    

    # print(pd.Index.difference(word_a_df["words"][0], utt_a_df["words"][0]))

    # for turn_set, tcu_set in turn_a_df["words"], turn_a_df["words"]:
        # print(turn_set - tcu_set) # sets lose ordering 
    # list_of_tuples = list(zip(turn_a_df["words"], tcu_a_df["words"]))

    # additions=[x for x in target if x not in current]
    # deletions=[x for x in current if x not in target]
    
    

    # print(f"hello, we have\n {utt_a_df.head(10)} and\n{word_a_df.head(5)}")
    # print(correct_differences(utt_a_df["words"][0], word_a_df["words"][0]))
    # print(word_a_df["words"][1])
    # print(correct_differences(utt_a_df["words"][1], word_a_df["words"][1]))
    # print(f"{turn_a_df}")
    
    # for tuple in list_of_tuples:
    #     print(tuple)

        # may be useful for debugging to have output options
        # as pd.Dataframe or csv

merge(utt_path, word_A_path, word_B_path)



# from dataclasses import dataclass
#
# import datasets
# from datasets import Value, Audio, Array3D
#
# from data_pipelines.datasets.switchboard.readers import (
#     ISIPAlignedCorpusReader,
#     LDCAudioCorpusReader
# )
#
#
# _LDC_HOMEPAGE = "https://catalog.ldc.upenn.edu/LDC97S62"
# _LDC_DESCRIPTION = """\
#     The Switchboard-1 Telephone Speech Corpus (LDC97S62) consists of\
#     approximately 260 hours of speech and was originally\
#     collected by Texas Instruments in 1990-1, under DARPA\
#     sponsorship
#     """
# _LDC_CITATION = """\
#     J. J. Godfrey, E. C. Holliman and J. McDaniel, "SWITCHBOARD: telephone\
#     speech corpus for research and development," [Proceedings] ICASSP-92: 1992\
#     IEEE International Conference on Acoustics, Speech, and Signal Processing,\
#      1992, pp. 517-520 vol.1, doi: 10.1109/ICASSP.1992.225858."""
#
#
# _LDC_AUDIO_CORPUS_URL = "https://catalog.ldc.upenn.edu/LDC97S62"
#
# class SwitchboardConfig(datasets.BuilderConfig):
#     def __init__(self, homepage, description, citation, data_url, features,
#             **kwargs):
#         super().__init__(**kwargs)
#         self.homepage = homepage
#         self.description = description
#         self.citation = citation
#         self.data_url = data_url
#         self.features = features
#
# class Switchboard(datasets.GeneratorBasedBuilder):
#
#     BUILDER_CONFIGS = [
#         SwitchboardConfig(
#             name="isip-aligned",
#             homepage = "https://isip.piconepress.com/projects/switchboard/",
#             description = """`\
#                 Several lexicon items were fixed in the 10/19/02 release, and\
#                 about 45 start/stop times that had negative durations\
#                 (stop time preceded the start time) were repaired. We are no\
#                 longer actively developing this resource, but continue to\
#                 include bug fixes. Included in this release are the final\
#                 transcriptions for the entire database, the complete lexicon,\
#                 and automatic word alignments.
#                 """ + "\n" + _LDC_DESCRIPTION,
#             citation=_LDC_CITATION,
#             data_url="https://www.isip.piconepress.com/projects/switchboard/releases/switchboard_word_alignments.tar.gz",
#             features={
#                 "session" : Value("string"),
#                 "participant" : Value("string"),
#                 "turns" : [{
#                     "start" : Value('float'),
#                     "end" : Value("float"),
#                     "text" : Value("string"),
#                     "tokens" : [{
#                         "start" : Value('float'),
#                         "end" : Value("float"),
#                         "text" : Value("string"),
#                     }]
#                 }]
#             },
#         ),
#         # NOTE: The ldc-audio requires the unzipped data directory path for now.
#         SwitchboardConfig(
#             name="ldc-audio",
#             homepage=_LDC_HOMEPAGE,
#             description=_LDC_DESCRIPTION,
#             citation=_LDC_CITATION,
#             data_url="",
#             features={
#                 "session" : Value('string'),
#                 "participant" : Value('string'),
#                 "audio_paths" : {
#                     "stereo" : Value('string'),
#                     "mono" : Value('string')
#                 },
#             },
#         )
#     ]
#
#     ############################ Overridden Methods ##########################
#
#     @property
#     def manual_download_instructions(self):
#         if self.config.name == "ldc-audio":
#             return (
#                 f"To use some variants of the Switchboard, you have to download "
#                 f"it manually. The audio is available at {_LDC_AUDIO_CORPUS_URL}."
#             )
#
#     def _info(self):
#         return datasets.DatasetInfo(
#             description=self.config.description,
#             citation=self.config.citation,
#             homepage=self.config.homepage,
#             features=datasets.Features(self.config.features)
#         )
#
#     def _split_generators(self, dl_manager : datasets.DownloadManager):
#         # Initialize the specific type of corpus.
#         # Select the reader
#         if self.config.name == "isip-aligned":
#             extracted_path = dl_manager.download_and_extract(self.config.data_url)
#             print(extracted_path)
#             self.reader = ISIPAlignedCorpusReader(extracted_path)
#         elif self.config.name == "ldc-audio":
#             extracted_path = self.config.data_dir
#             if not os.path.isdir(extracted_path):
#                 raise FileNotFoundError(
#                     f"{extracted_path} does not exist. Make sure you insert "
#                     f"a manual dir via `datasets.load_dataset('matinf', data_dir=...)` "
#                     f"Manual download instructions: {self.manual_download_instructions}"
#                 )
#             self.reader = LDCAudioCorpusReader(extracted_path)
#         else:
#             raise NotImplementedError()
#         sessions = self.reader.get_sessions()
#         return [
#             datasets.SplitGenerator(
#                 name="full",
#                 gen_kwargs={"sessions" : sessions})
#         ]
#
#     def _generate_examples(self, sessions):
#         for session in sessions:
#             for participant in self.reader.PARTICIPANTS:
#                 if self.config.name == "isip-aligned":
#                     conv = self.reader.get_session_transcript(
#                         session,participant)
#                     yield f"{session}_{participant}", {
#                         "session" : session,
#                         "participant" : participant,
#                         "turns" : conv
#                     }
#                 elif self.config.name == "ldc-audio":
#                     mono_path = self.reader.mono_paths[session][participant]
#                     yield f"{session}_{participant}",{
#                         "session" : session,
#                         "participant" : participant,
#                         "audio_paths" : {
#                             "stereo" : self.reader.wav_paths[session],
#                             "mono" : mono_path
#                         },
#                     }
#                 else:
#                     raise NotImplementedError()
#
#
# _DEFAULT_FEATURES = {
#     "id" : Value('string'),
#     "utterances" : [{
#             "speaker" : Value("string"),
#             "start" : Value("float"),
#             "end" : Value("float"),
#             "text" : Value("string"),
#         }
#     ],
# }
#
# _AUDIO_FEATURES = {
#     "id" : Value('string'),
#     "path" : Value("string"),
# }