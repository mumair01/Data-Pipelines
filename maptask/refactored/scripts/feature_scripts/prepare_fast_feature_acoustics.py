# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-05-12 19:49:23
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-13 09:06:13

import os
import sys
import pandas as pd
import numpy as np
import h5py
from vardefs import *
from utils import *


def prepare_data_acoustics_from_files(voice_activity_annotation_path, raw_gemaps_path):

    # Creating output dataset file
    filename = os.path.splitext(
        os.path.basename(voice_activity_annotation_path))[0]
    split_indices = []
    annotation_df = pd.read_csv(voice_activity_annotation_path, delimiter=",")
    feature_df = pd.read_csv(raw_gemaps_path, delimiter=",")
    for frame_time in annotation_df["frameTimes"][1:]:
        split_indices.append(
            np.max(np.where(feature_df['frameTime'] < frame_time)) + 1)
    data_split_list = np.split(feature_df, split_indices)
    max_len = find_max_len(data_split_list)
    data_dict = {
        'filename': filename,
        'x': {},
        'x_i': {}
    }
    for feature_name in GEMAP_FULL_FEATURES:
        data_dict['x'][feature_name] = np.zeros(
            (len(annotation_df["frameTimes"]), max_len))
        data_dict['x_i'][feature_name] = np.zeros(
            (len(annotation_df["frameTimes"]), max_len))
        for ind, data_split in enumerate(data_split_list):
            data_dict['x'][feature_name][ind, :len(
                data_split)] = data_split[feature_name]
    return data_dict
