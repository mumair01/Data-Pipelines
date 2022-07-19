# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-03-04 18:34:10
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-03-04 18:54:41
import os
import sys
import shutil
from utils import *


def continue_index(content):
    # If the content lines have a '+' dialogue act,
    # return the index
    # else return False
    for index, line in enumerate(content):
        parts = line.split()
        if parts[0] == '+' or parts[0] == "+@" or parts[0] == "+*":
            return index
    return False


def propagate_continuations(file_name):

    def prev_or_next(content, cont_index, prev_index, next_index):
        # cont -- the utterance line with a '+' act
        # prev_utt -- the utterance before the continuation
        # next_utt -- the utterance following the continuation
        # Return "next" or "prev" based on matching heuristics

        cont = content[cont_index]
        try:
            prev_utt = content[prev_index]
        except IndexError:
            prev_utt = False

        try:
            next_utt = content[next_index]
        except IndexError:
            next_utt = False

        if (not prev_utt) and (not next_utt):
            print("Error: No previous or next utterance for continuation")
            sys.exit(1)
        elif not prev_utt:
            return "next"
        elif not next_utt:
            return "prev"
        else:
            cont_split = cont.split()
            cont_utt = int(cont_split[2][3:-1])
            cont_words = cont_split[3:]

            prev_split = prev_utt.split()
            prev_utt = prev_split[2][3:-1]
            prev_words = prev_split[3:]

            next_split = next_utt.split()
            next_act = next_split[0]
            next_utt = int(next_split[2][3:-1])
            next_words = next_split[3:]

            if next_utt > 1:
                # Continuations are in different utterances
                return "prev"
            if cont_utt > 1:
                return "next"
            if (not prev_words[-1] == "/") and cont_words[-1] == "/":
                # Complete utterances usually end in "/", so continuations lack them
                return "prev"
            if not cont_words[-1] == "/":
                return "next"
            # Note: The above should cover 99% of cases.
            # The manual suggests that the '/' marker should be used for
            # end of TCU, but there were a handful of errors, so the
            # following heuristics were kept to handle those cases
            if cont_words[0] == prev_words[-1]:
                # If the final symbol matches
                return "prev"
            if cont_words[-1] == next_words[0]:
                return "next"
            if "." in " ".join(prev_words)[-5:]:
                # Utterance was transcribed as a sentence
                return "next"
            if "." in " ".join(cont_words)[-5:]:
                return "prev"
            if "?" in " ".join(prev_words)[-5:]:
                # Utterance was transcribed as a sentence
                return "next"
            if "?" in " ".join(cont_words)[-5:]:
                return "prev"
            if len(prev_words) > 1 and cont_words[0] == prev_words[-2]:
                # Penultimate symbol matches
                # Sometimes final is markup instead of word
                return "prev"
            if len(cont_words) > 1 and cont_words[-2] == next_words[0]:
                return "next"
            if next_act == '+':
                # If continuation of continuation, assume continuation of previous
                return "prev"

            print("took the easy path")
            print(cont)
            if len(prev_words) < len(next_words):
                return "prev"
            return "next"

    def merge_utts(cont, tagged, prev_or_next):
        # cont -- the utterance line with a '+' act
        # tagged -- the utterance of which it is a continuation
        # prev_or_next -- if continue is first, "prev", else "next"
        cont_split = cont.split()
        cont_speaker = cont_split[1][0]
        cont_words = cont_split[3:]

        tagged_split = tagged.split()
        tagged_act = tagged_split[0]
        tagged_num = tagged_split[1][2:]
        tagged_utt = tagged_split[2][3:-1]
        tagged_words = tagged_split[3:]

        # print(tagged_act)

        if prev_or_next == "prev":
            new_words = " ".join(tagged_words + cont_words)
            return f"{tagged_act}\t{cont_speaker}.{tagged_num} utt{tagged_utt}: {new_words}"
        new_words = " ".join(cont_words + tagged_words)
        return "{tagged_act}\t{cont_speaker}.{cont_num} utt{cont_utt}: {new_words}"

    with open(file_name, 'r', encoding="UTF-8") as lc_file:
        lines = lc_file.readlines()

    content = []
    start = False
    output = ""
    for line in lines:
        if start:
            if not line.strip() == "":
                content.append(line.strip())
        else:
            output += line
            if not start and "====" in line:
                start = True

    while True:
        cont_index = continue_index(content)
        if not cont_index:
            break

        cont = content[cont_index]
        # The first letter of the second 'word' is
        cont_speaker = cont.split()[1][0]
        # the speaker letter

        prev_index = cont_index
        while True:
            prev_index -= 1
            try:
                prev_speaker = content[prev_index].split()[1][0]
                if prev_speaker == cont_speaker:
                    break
            except IndexError:
                # The continuation was the first utterance
                prev_speaker = False
                break

        next_index = cont_index
        while True:
            next_index += 1
            try:
                next_speaker = content[next_index].split()[1][0]
                if next_speaker == cont_speaker:
                    break
            except IndexError:
                # The continuation was the last utterance
                next_speaker = False
                break

        p_or_n = prev_or_next(content,
                              cont_index,
                              prev_index,
                              next_index)
        if p_or_n == "prev":
            new_utt = merge_utts(cont, content[prev_index], p_or_n)
            content[prev_index] = new_utt
            del content[cont_index]
        elif p_or_n == "next":
            new_utt = merge_utts(cont, content[next_index], p_or_n)
            content[cont_index] = new_utt
            del content[next_index]
        else:
            print("Error: Not prev or next")
            sys.exit(1)

    return output + "\n".join(content)


def re_utterize_lc_data(src_dir, dst_dir):
    if not os.path.isdir(src_dir):
        return
    os.makedirs(dst_dir, exist_ok=True)
    # Obtain all files with the .utt extension
    file_paths = get_files_with_ext(src_dir, ".utt")
    for path in file_paths:
        new_data = propagate_continuations(path)
        with open(os.path.join(dst_dir, os.path.basename(path)),
                  "w", encoding="UTF-8") as f:
            f.write(new_data)
