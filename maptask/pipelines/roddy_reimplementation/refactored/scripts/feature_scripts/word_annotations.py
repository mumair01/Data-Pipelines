# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-05-13 09:55:25
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-13 10:02:12

import numpy as np
from utils import *
import xml.etree.ElementTree
import nltk
import pandas as pd

# CONSTANTS
MAX_LENGTH = 2
FRAME_DELAY = 2  # NOTE: This is somehow adding delay to the features.


def get_word_annotations_from_file(processed_gemap_path, timed_unit_path,
                                   word_to_ix, output_dir):

    filename = os.path.splitext(os.path.basename(processed_gemap_path))[0]
    frame_times = np.array(
        pd.read_csv(processed_gemap_path, delimiter=",", usecols=[1])['frameTime'])
    word_values = np.zeros((len(frame_times), MAX_LENGTH))
    tree = xml.etree.ElementTree.parse(timed_unit_path).getroot()
    for annotation_type in tree.findall('tu'):
        word_frame_list = []
        target_word = annotation_type.text.strip()
        if "--" in target_word:
            word_frame_list.append('--disfluency_token--')
        else:
            word_frame_list.extend(nltk.word_tokenize(target_word))
        # Get the token values for the words
        current_words_idx = [word_to_ix[word] for word in word_frame_list]
        # Process
        end_idx_advanced = find_nearest(frame_times, float(
            annotation_type.get('end'))) + FRAME_DELAY
        if end_idx_advanced < len(word_values):
            if np.min(np.where(word_values[end_idx_advanced] == 0)[0] > 0):
                pass
            arr_start_idx = np.min(
                np.where(word_values[end_idx_advanced] == 0)[0])
            arr_end_idx = arr_start_idx + len(current_words_idx)
            if arr_end_idx < MAX_LENGTH:
                word_values[end_idx_advanced][arr_start_idx:arr_end_idx] = np.array(
                    current_words_idx)
        # Prepare and write the output files
        output_df = pd.DataFrame(np.concatenate(
            [np.expand_dims(frame_times, 1), word_values], 1).transpose())
        output_df = np.transpose(output_df)  # NOTE This seems redundant
        output_df.columns = ['frameTimes'] + \
            [str(n) for n in range(MAX_LENGTH)]
        output_df.to_csv("{}/{}.csv".format(output_dir, filename,
                         float_format="%.6f", sep=",", index=False, header=True))
