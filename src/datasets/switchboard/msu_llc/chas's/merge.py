# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-03-03 09:54:27
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-03-23 09:28:00
"""

TODO: There seems to be an off-by-one error where this script is
      omitting the final utterance for each speaker

merge.py takes the data from the Linguistic Consortium transcripts
and the Mississippi State transcripts and attempts to put timing
and dialogue act annotations into a single file.

We want to do this so that we can model the dialogue act information
and timing information in the same model.

Since the transcripts are of the same information, but significantly
different, we use a series of heuristics to find matching words to use
for timing information. The first is matching the transcripts themselves.
According to the documentation, the transcripts have conversation numbers
which we use to matchs the LC file to the MSU file. Then, we use the
word-by-word timing information in MSU and attempt to match start and end
words of the LC utterances in order to get timing information. The
word-by-word accuracy and error rates are tracked and only transcripts
which high accuracy (>90%) and low error (<2%) are output. Accuracy rates
here are exact word matches and error rates are words that match no heuristic.

The other heuristics are:
1. A word missing from one of the transcripts, but not the other.
2. A word is abandoned in one transcript and spelled out in another
3. A weak version of alternative spellings where the length is the same
   and the start letter is the same
4. A word is repeated in one transcript but not the other.

Because the accuracy threshold is high and the error threshold is low
for outputting a file, only 66 conversations are currently being output
If we improve the heuristics, we can probably grow the available dataset.

Note that we only need these conversations for questions the involve the
intersection of dialogue acts and timing. If we want to model dialogue acts
with n-grams or other HMMs or word-models, the timing is not relevant.
"""

import os
import sys
import re


def merge_corpora(base_dir, lc_src, msu_src, output_dir):
    """ Given a base directory and directories for the Linguistic
    Consortium data and MSU data, write a set of merged transcripts
    into the output directory that use data from both, when able """

    # For an utterance, process the text into a logical data structure
    def process_line(line):
        split_line = line.strip().split()
        speech_act = split_line[0]
        speaker = split_line[1].split('.')[0]
        utt_num = split_line[1].split('.')[1]
        tcu_num = split_line[2][3:-1]
        words = []
        for word in split_line[3:]:
            if word[-1] != "-":
                # We will match abandoned words
                word = re.sub('-', ' ', word)
            word = re.sub('--', '', word)
            word = re.sub('#', '', word)
            word = re.sub('{[A-Z]', '', word)
            word = re.sub('<[a-z]*\>', '', word)
            word = re.sub('[(),+/?.{}\[\]]', '', word)
            if not word.strip() == "":
                words.append(word.lower())
        return {"speech_act": speech_act,
                "speaker": speaker,
                "utt_num": utt_num,
                "tcu_num": tcu_num,
                "words": words}

    def get_dialogue_acts(file_name, speaker):
        dialogue_acts = []
        with open(file_name, 'r', encoding="UTF-8") as speech_act_file:
            speech_act_text = speech_act_file.readlines()
        for utterance in speech_act_text:
            if f"{speaker}." in utterance:
                dialogue_acts.append(process_line(utterance))

        return dialogue_acts

    def get_timing(file_name):

        with open(file_name, 'r', encoding="UTF-8") as timing_file:
            timing_lines = timing_file.readlines()

        speaker_timing = []
        for line in timing_lines:
            split_line = line.split()
            word = split_line[3].lower()
            if not (word[0] == "[" and word[-1] == "]"):
                convo_id = split_line[0]
                start = split_line[1]
                end = split_line[2]

                if word[-1] != "-":
                    # We will match abandoned words
                    word = re.sub('-', ' ', word)
                    # word = re.sub("\[\]-", '', word)

                utt_dict = {"convo_id": convo_id,
                            "start": start,
                            "end": end,
                            "word": word}
                speaker_timing.append(utt_dict)

        return speaker_timing

    def get_dialogue_act_word(dialogue_acts, index):
        utt_num = 0
        while True:
            try:
                num_words = len(dialogue_acts[utt_num]["words"])
            except IndexError:
                return (None, None, None)
            if index < 0:
                return None
            if index < num_words:
                return (dialogue_acts[utt_num]["words"][index],
                        utt_num,
                        dialogue_acts[utt_num]["speech_act"])

            index -= num_words
            utt_num += 1

    def match_corpus(dialogue_acts, timing, speaker, word_cases):
        timing_index = 0
        dialogue_act_index = 0
        utts = []
        current_words = []
        current_start = None
        current_end = None
        current_act = None
        current_utt = None

        prev_timing_word = None
        prev_dialogue_act_word = None

        while True:

            (dialogue_act_word1, utt1, act1) = \
                get_dialogue_act_word(dialogue_acts, dialogue_act_index)

            (dialogue_act_word2, utt2, act2) = \
                get_dialogue_act_word(dialogue_acts, dialogue_act_index+1)

            # Update timing vars
            try:
                timing_word1 = timing[timing_index]["word"]
            except IndexError:
                # All timing words have been accounted for
                break
            try:
                timing_word2 = timing[timing_index + 1]["word"]
            except IndexError:
                timing_word2 = None
            if dialogue_act_word1 == timing_word1:
                # Case 1: Words match
                if utt1 != current_utt and len(current_words) != 0:
                    utts.append({"speaker": speaker,
                                 "start": current_start,
                                 "end": current_end,
                                 "words": " ".join(current_words),
                                 "speech_act": current_act})
                    current_start = timing[timing_index]["start"]
                    current_words = []
                current_end = timing[timing_index]["end"]
                current_words.append(timing_word1)
                current_act = act1
                current_utt = utt1
                timing_index += 1
                dialogue_act_index += 1
                word_cases["Case 1"] += 1
            elif dialogue_act_word1 == timing_word2:
                # Case 2: Timing has missing word
                if utt1 != current_utt:
                    utts.append({"speaker": speaker,
                                 "start": current_start,
                                 "end": current_end,
                                 "words": " ".join(current_words),
                                 "speech_act": current_act})
                    current_start = timing[timing_index]["start"]
                    current_words = []
                current_end = timing[timing_index]["end"]
                current_words.append(timing_word1)
                current_words.append(timing_word2)
                current_act = act1
                current_utt = utt1
                timing_index += 2
                dialogue_act_index += 1
                word_cases["Case 2"] += 1
            elif dialogue_act_word2 == timing_word1:
                # Case 3: Dialogue Act has missing word
                if utt2 != current_utt:
                    if current_act is not None:
                        utts.append({"speaker": speaker,
                                     "start": current_start,
                                     "end": current_end,
                                     "words": " ".join(current_words),
                                     "speech_act": current_act})
                    current_start = timing[timing_index]["start"]
                    current_words = []
                current_end = timing[timing_index]["end"]
                current_words.append(timing_word1)
                current_act = act2
                current_utt = utt2
                timing_index += 1
                dialogue_act_index += 2
                word_cases["Case 3"] += 1
            elif dialogue_act_word1 and "-" in timing_word1 and \
                    timing_word1[0] == dialogue_act_word1[0]:
                # Case 4: Timing word is abandoned,
                #  but matches dialogue act word start letter
                if utt2 != current_utt:
                    utts.append({"speaker": speaker,
                                 "start": current_start,
                                 "end": current_end,
                                 "words": " ".join(current_words),
                                 "speech_act": current_act})
                    current_start = timing[timing_index]["start"]
                    current_words = []
                current_end = timing[timing_index]["end"]
                current_words.append(timing_word1)
                current_act = act1
                current_utt = utt1
                timing_index += 1
                dialogue_act_index += 1
                word_cases["Case 4"] += 1
            elif timing_word1 and dialogue_act_word1 and \
                    len(timing_word1) == len(dialogue_act_word1) and \
                    timing_word1[0] == dialogue_act_word1[0]:
                # Case 5: alternative transcription
                if utt2 != current_utt:
                    utts.append({"speaker": speaker,
                                 "start": current_start,
                                 "end": current_end,
                                 "words": " ".join(current_words),
                                 "speech_act": current_act})
                    current_start = timing[timing_index]["start"]
                    current_words = []
                current_end = timing[timing_index]["end"]
                current_words.append(timing_word1)
                current_act = act1
                current_utt = utt1
                timing_index += 1
                dialogue_act_index += 1
                word_cases["Case 5"] += 1
            elif dialogue_act_word1 and \
                    prev_dialogue_act_word == dialogue_act_word1:
                # Case 6: Dialogue act word repeat
                current_act = act1
                current_utt = utt1
                dialogue_act_index += 1
                word_cases["Case 6"] += 1
            elif timing_word1 and \
                    prev_timing_word == timing_word1:
                # Case 7: Timing word repeat
                current_end = timing[timing_index]["end"]
                current_words.append(timing_word1)
                timing_index += 1
                word_cases["Case 7"] += 1
            else:
                # Case 8: Default
                current_words.append(timing_word1)
                if not current_start:
                    current_start = timing[timing_index]["start"]
                current_end = timing[timing_index]["end"]
                timing_index += 1
                word_cases["Case 8"] += 1

            prev_timing_word = timing_word1
            prev_dialogue_act_word = dialogue_act_word1

        return utts, word_cases

    def output_cha(utts, quality, convo_num, files):
        """Output merged files into .cha file."""
        output = "@Begin\n"
        output += "@Languages:\teng\n"
        output += \
            "@Participants:\tSPA SPA Unidentified, SPB SPB Unidentified\n"
        output += \
            "@ID:\teng|Switchboard_Corpus|SPA||unknown||Unidentified|||\n"
        output += \
            "@ID:\teng|Switchboard_Corpus|SPB||unknown||Unidentified|||\n"
        for key in quality:
            output += f"@{key}:\t{quality[key]}\n"
        output += f"@DialogueActSource:\t{files['da']}\n"
        output += f"@TimingSourceA:\t{files['t_a']}\n"
        output += f"@TimingSourceB:\t{files['t_b']}\n"
        output += "@New Episode\n"

        utts = list(filter(lambda x: x["start"] is not None, utts))
        utts.sort(key=lambda x: float(x["start"]))

        for utt in utts:
            output += "*SP{0}:\t{1} •{2}_{3}•\n%dml:\t{4}\n".format(
                utt["speaker"],
                utt["words"],
                round(float(utt["start"]) * 1000),
                round(float(utt["end"]) * 1000),
                utt["speech_act"])
        output += "@End"
        with open(base_dir + output_dir + f"{convo_num}.cha", 'w+',
                  encoding="UTF-8") as output_file:
            output_file.write(output)

    # successes = 0

    dialogue_act_data_file_list = \
        [x for x in os.listdir(base_dir + lc_src) if ".utt" in x]
    timing_data_file_list = \
        [x for x in os.listdir(base_dir + msu_src) if "word.text" in x]

    convo_nums = []
    for timing_file in timing_data_file_list:
        print(timing_file)
        convo_nums.append(timing_file[2:6])

    convo_nums = list(set(convo_nums))

    problems = 0
    matched = 0
    low_quality = 0
    quantiles = {"0.9": {"Case 1": 0,
                         "Case 2": 0,
                         "Case 3": 0,
                         "Case 4": 0,
                         "Case 5": 0,
                         "Case 6": 0,
                         "Case 7": 0,
                         "Case 8": 0},
                 "0.8": {"Case 1": 0,
                         "Case 2": 0,
                         "Case 3": 0,
                         "Case 4": 0,
                         "Case 5": 0,
                         "Case 6": 0,
                         "Case 7": 0,
                         "Case 8": 0},
                 "0.7": {"Case 1": 0,
                         "Case 2": 0,
                         "Case 3": 0,
                         "Case 4": 0,
                         "Case 5": 0,
                         "Case 6": 0,
                         "Case 7": 0,
                         "Case 8": 0},
                 "0.6": {"Case 1": 0,
                         "Case 2": 0,
                         "Case 3": 0,
                         "Case 4": 0,
                         "Case 5": 0,
                         "Case 6": 0,
                         "Case 7": 0,
                         "Case 8": 0},
                 "0.5": {"Case 1": 0,
                         "Case 2": 0,
                         "Case 3": 0,
                         "Case 4": 0,
                         "Case 5": 0,
                         "Case 6": 0,
                         "Case 7": 0,
                         "Case 8": 0},
                 "0.4": {"Case 1": 0,
                         "Case 2": 0,
                         "Case 3": 0,
                         "Case 4": 0,
                         "Case 5": 0,
                         "Case 6": 0,
                         "Case 7": 0,
                         "Case 8": 0},
                 "0.3": {"Case 1": 0,
                         "Case 2": 0,
                         "Case 3": 0,
                         "Case 4": 0,
                         "Case 5": 0,
                         "Case 6": 0,
                         "Case 7": 0,
                         "Case 8": 0},
                 "0.2": {"Case 1": 0,
                         "Case 2": 0,
                         "Case 3": 0,
                         "Case 4": 0,
                         "Case 5": 0,
                         "Case 6": 0,
                         "Case 7": 0,
                         "Case 8": 0},
                 "0.1": {"Case 1": 0,
                         "Case 2": 0,
                         "Case 3": 0,
                         "Case 4": 0,
                         "Case 5": 0,
                         "Case 6": 0,
                         "Case 7": 0,
                         "Case 8": 0},
                 "0": {"Case 1": 0,
                       "Case 2": 0,
                       "Case 3": 0,
                       "Case 4": 0,
                       "Case 5": 0,
                       "Case 6": 0,
                       "Case 7": 0,
                       "Case 8": 0}}

    num_files = len(timing_data_file_list)
    for zed, timing_file in enumerate(timing_data_file_list):
        print(f"{zed} / {num_files}\t{timing_file}")
        convo_num = timing_file[2:6]
        matches = [x for x in dialogue_act_data_file_list if convo_num in x]
        num_matches = len(matches)
        if num_matches == 0:
            problems += 1
            continue
        if num_matches > 1:
            continue
        if num_matches == 1:
            try:
                dialogue_act_file = os.path.join(base_dir + lc_src,
                                                 matches[0])
                timing_file_a = base_dir + msu_src + \
                    f"sw{convo_num}A-ms98-a-word.text"
                timing_file_b = base_dir + msu_src + \
                    f"sw{convo_num}B-ms98-a-word.text"
                speaker_a_dialogue_acts = get_dialogue_acts(dialogue_act_file,
                                                            "A")

                speaker_b_dialogue_acts = get_dialogue_acts(dialogue_act_file,
                                                            "B")
                speaker_a_timing = get_timing(timing_file_a)

                speaker_b_timing = get_timing(timing_file_b)
                word_cases1 = {"Case 1": 0,
                               "Case 2": 0,
                               "Case 3": 0,
                               "Case 4": 0,
                               "Case 5": 0,
                               "Case 6": 0,
                               "Case 7": 0,
                               "Case 8": 0}
                match_a1, word_cases1 = match_corpus(speaker_a_dialogue_acts,
                                                     speaker_a_timing,
                                                     "A",
                                                     word_cases1)

                match_b1, word_cases1 = match_corpus(speaker_b_dialogue_acts,
                                                     speaker_b_timing,
                                                     "B",
                                                     word_cases1)
                total1 = 0
                for key in word_cases1.keys():
                    total1 += word_cases1[key]
                word_cases2 = {"Case 1": 0,
                               "Case 2": 0,
                               "Case 3": 0,
                               "Case 4": 0,
                               "Case 5": 0,
                               "Case 6": 0,
                               "Case 7": 0,
                               "Case 8": 0}
                match_a2, word_cases2 = match_corpus(speaker_b_dialogue_acts,
                                                     speaker_a_timing,
                                                     "A",
                                                     word_cases2)
                match_b2, word_cases2 = match_corpus(speaker_a_dialogue_acts,
                                                     speaker_b_timing,
                                                     "B",
                                                     word_cases2)
                total2 = 0
                for key in word_cases2.keys():
                    print("key", key)
                    total2 += word_cases2[key]
                print("measure_1", word_cases1["Case 1"] /
                      total1, word_cases1["Case 1"], total1)
                measure1 = word_cases1["Case 1"] / total1
                measure2 = word_cases2["Case 1"] / total2
                print("measure_2", word_cases2["Case 1"] /
                      total2, word_cases2["Case 1"], total2)
                if measure1 > measure2:
                    word_cases = word_cases1
                    matches = match_a1 + match_b1
                    print("CASE-1")
                else:
                    word_cases = word_cases2
                    matches = match_a2 + match_b2
                    print("CASE-2")
                total = 0
                for key in word_cases.keys():
                    total += word_cases[key]
                quality1 = word_cases["Case 1"] / total
                quality2 = word_cases["Case 2"] / total
                quality3 = word_cases["Case 3"] / total
                quality4 = word_cases["Case 4"] / total
                quality5 = word_cases["Case 5"] / total
                quality6 = word_cases["Case 6"] / total
                quality7 = word_cases["Case 7"] / total
                quality8 = word_cases["Case 8"] / total
                for i, qual in enumerate([quality1, quality2, quality3,
                                          quality4, quality5, quality6,
                                          quality7, quality8]):
                    # Separating here based on the quality level that is
                    # prefered later on.
                    if qual > 0.9:
                        quantiles["0.9"][f"Case {i+1}"] += 1
                    elif qual > 0.8:
                        quantiles["0.8"][f"Case {i+1}"] += 1
                    elif qual > 0.7:
                        quantiles["0.7"][f"Case {i+1}"] += 1
                    elif qual > 0.6:
                        quantiles["0.6"][f"Case {i+1}"] += 1
                    elif qual > 0.5:
                        quantiles["0.5"][f"Case {i+1}"] += 1
                    elif qual > 0.4:
                        quantiles["0.4"][f"Case {i+1}"] += 1
                    elif qual > 0.3:
                        quantiles["0.3"][f"Case {i+1}"] += 1
                    elif qual > 0.2:
                        quantiles["0.2"][f"Case {i+1}"] += 1
                    elif qual > 0.1:
                        quantiles["0.1"][f"Case {i+1}"] += 1
                    else:
                        quantiles["0"][f"Case {i+1}"] += 1
                error_rate = word_cases["Case 8"] / total
                if error_rate > 0.05:
                    low_quality += 1
                matched += 1
                qualities = {"ExactMatch": quality1,
                             "TimingOmission": quality2,
                             "DialogueActOmission": quality3,
                             "TimingAbandon": quality4,
                             "AlternativeTranscription": quality5,
                             "DialogueActRepeat": quality6,
                             "TimingRepeat": quality7,
                             "WordError": quality8}
                files = {"da": dialogue_act_file,
                         "t_a": timing_file_a,
                         "t_b": timing_file_b}
                output_cha(matches, qualities, convo_num, files)
            except IndexError:
                pass

    # for case in list(map(lambda x: x + 1, list(range(8)))):
    #     print("\n\nCase {0}".format(case))
    #     for key in sorted(list(quantiles.keys())):
    #         print(f"{0}:\t{1}".format(key,
    # quantiles[key]["Case {0}".format(case)]))
    # print("{0} total problems of {1} convos".format(problems,
    # len(convo_nums)))
    # print("{0} matched convos".format(matched))

    # print(f"{successes} successful merges")


if __name__ == "__main__":
    merge_corpora("/home/chas/Projects/Switchboard/",
                  "lc-sb2/",
                  "msu-sb/",
                  "new-sb/")
