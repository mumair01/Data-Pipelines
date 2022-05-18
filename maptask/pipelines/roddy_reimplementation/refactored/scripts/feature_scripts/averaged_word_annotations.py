# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-05-13 10:17:49
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-13 10:37:01


import os
import numpy as np
import pandas as pd
import pickle
from multiprocess import Pool


def get_local_set_from_file(word_annotation_path):
    assert os.path.isfile(word_annotation_path)
    word_annotations_df = pd.read_csv(word_annotation_path, delimiter=",")
    combinations = np.array(word_annotations_df[word_annotations_df.columns[1:]])[list(
        set(np.nonzero(np.array(word_annotations_df[word_annotations_df.columns[1:]]))[0]))]
    local_set = [frozenset(i) for i in combinations]
    return local_set


def get_average_word_annotations_from_file(
        processed_gemap_path, word_annotation_path, total_set, output_dir):
    assert os.path.isfile(processed_gemap_path)
    assert os.path.isfile(word_annotation_path)
    # Create new average glove embeddings dictionary.
    set_dict = dict()  # NOTE: Not sure what this is.
    for idx, glove_combination in enumerate(total_set):
        set_dict[glove_combination] = idx+1
    set_dict[frozenset([0])] = 0
    pickle.dump(set_dict, open(os.path.join(output_dir, "set_dict.p"), 'wb'))
    filename = os.path.splitext(os.path.basename(processed_gemap_path))[0]
    word_annotations_df = pd.read_csv(word_annotation_path, delimiter=",")
    frame_times = word_annotations_df['frameTimes']
    avg_word_annotations = np.zeros(frame_times.shape)
    indices = list(set(np.nonzero(
        np.array(word_annotations_df[word_annotations_df.columns[1:]]))[0]))
    for idx in indices:
        avg_word_annotations[idx] = set_dict[
            frozenset(np.array(word_annotations_df[word_annotations_df.columns[1:]])[idx])]
    output_df = pd.DataFrame(
        np.vstack([frame_times, avg_word_annotations]).transpose())
    output_df.columns = ['frameTimes', 'word']
    output_df.to_csv(os.path.join(output_dir, "{}.csv".format(
        filename)), float_format='%.6f', sep=',', index=False, header=True)
