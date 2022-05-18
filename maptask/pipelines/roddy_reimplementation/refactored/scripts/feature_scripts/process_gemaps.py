# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-05-12 16:29:21
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-12 19:51:53

import os
import pandas as pd
from sklearn import preprocessing
from vardefs import *


def process_gemaps_from_file(feature_file_path,  raw_features_dir, z_normalized_dir, z_normalized_pooled_dir):
    # Create dirs
    filename = os.path.splitext(os.path.basename(feature_file_path))[0]
    gemaps_df = pd.read_csv(feature_file_path, delimiter=",")
    # Extract all the raw required features
    full_features_raw_df = gemaps_df[GEMAP_FULL_FEATURES]
    full_features_raw_df.insert(1, 'frameTime', gemaps_df["frameTime"])
    full_features_raw_df.to_csv("{}/{}.csv".format(raw_features_dir, filename),
                                float_format="%.10f", sep=",", index=False, header=True)
    # Extract the z-normalized features
    z_normalized_features = dict()
    for feature in GEMAP_FULL_FEATURES:
        z_normalized_features[feature] = preprocessing.scale(
            full_features_raw_df[feature])
    z_normalized_df = pd.DataFrame(z_normalized_features)
    z_normalized_df.insert(1, 'frameTime', gemaps_df["frameTime"])
    z_normalized_df.to_csv("{}/{}.csv".format(z_normalized_dir, filename),
                           float_format="%.10f", sep=",", index=False, header=True)
    # TODO: Z-normalized pooled are not being generated - instead just writing existing data
    # as pooled for now.
    z_normalized_df.to_csv("{}/{}.csv".format(z_normalized_pooled_dir, filename),
                           float_format="%.10f", sep=",", index=False, header=True)
