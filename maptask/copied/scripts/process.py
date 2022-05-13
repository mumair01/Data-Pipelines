# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-05-08 16:29:41
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-11 14:38:16

import os
import sys
import opensmile
import audiofile
from pathlib import Path
import numpy as np
import pandas as pd
from tqdm import tqdm
import subprocess
import xml.etree.ElementTree
from sklearn import preprocessing
import h5py
import nltk
import pickle
import json

# CONSTANTS
FREQUENCY_FEATURES = ['F0semitoneFrom27.5Hz', 'jitterLocal', 'F1frequency',
                      'F1bandwidth', 'F2frequency', 'F3frequency']
FREQUENCY_MASK = [0, 0, 0, 0, 0, 0]
ENERGY_FEATURES = ['Loudness', 'shimmerLocaldB', 'HNRdBACF']
ENERGY_MASK = [0, 0, 0]
SPECTRAL_FEATURES = ['alphaRatio', 'hammarbergIndex', 'spectralFlux',
                     'slope0-500', 'slope500-1500', 'F1amplitudeLogRelF0',
                     'F2amplitudeLogRelF0', 'F3amplitudeLogRelF0', 'mfcc1',
                     'mfcc2', 'mfcc3', 'mfcc4']
SPECTRAL_MASK = [0, 0, 0, 0, 0, -201, -201, -201, 0, 0, 0, 0]
GEMAP_FULL_FEATURES = FREQUENCY_FEATURES + ENERGY_FEATURES + SPECTRAL_FEATURES


# NOTE: It looks like the purpose of this is to create some new embeddings
#
def get_average_word_annotations_from_file(
        feature_files, word_annotations_dir, word_to_ix, output_dir):
    def find_nearest(array, value):
        idx = (np.abs(array-value)).argmin()
        return idx
    # Collect corresponding annotation files for each feature file.
    collected_files = []
    for feature_file_path in feature_files:
        filename = os.path.splitext(os.path.basename(feature_file_path))[0]
        annotation_filename = "{}.csv".format(filename)
        annotation_path = os.path.join(
            word_annotations_dir, annotation_filename)
        if os.path.isfile(annotation_path):
            collected_files.append((feature_file_path, annotation_path))
    # Process the collected files
    total_list = []  # NOTE: Need to figure out what this total set is.
    for feature_file, word_annoation_file in collected_files:
        word_annotations_df = pd.read_csv(word_annoation_file, delimiter=",")
        combinations = np.array(word_annotations_df[word_annotations_df.columns[1:]])[list(
            set(np.nonzero(np.array(word_annotations_df[word_annotations_df.columns[1:]]))[0]))]
        local_set = [frozenset(i) for i in combinations]
        total_list.extend(local_set)
    total_set = set(total_list)
    # Create new average glove embeddings dictionary.
    set_dict = dict()  # NOTE: Not sure what this is.
    for idx, glove_combination in enumerate(total_set):
        set_dict[glove_combination] = idx+1
    set_dict[frozenset([0])] = 0
    for feature_file, word_annoation_file in collected_files:
        filename = os.path.splitext(os.path.basename(feature_file))[0]
        word_annotations_df = pd.read_csv(word_annoation_file, delimiter=",")
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
    # Outputing the set dictionary
    pickle.dump(set_dict, open(os.path.join(output_dir, "set_dict.p"), 'wb'))


# NOTE: This code is very similar to the get vocabulary one.


def get_word_annotations_from_files(feature_files, annotations_dir,
                                    word_to_ix, output_dir):
    def find_nearest(array, value):
        idx = (np.abs(array-value)).argmin()
        return idx
    # CONSTANTS
    MAX_LENGTH = 2
    FRAME_DELAY = 2  # NOTE: This is somehow adding delay to the features.
    # Collect corresponding annotation files for each feature file.
    collected_files = []
    for feature_file_path in feature_files:
        filename = os.path.splitext(os.path.basename(feature_file_path))[0]
        annotation_filename = "{}.timed-units.xml".format(filename)
        annotation_path = os.path.join(annotations_dir, annotation_filename)
        if os.path.isfile(annotation_path):
            collected_files.append((feature_file_path, annotation_path))
    # Process
    for feature_file, annotation_file in collected_files:
        filename = os.path.splitext(os.path.basename(feature_file))[0]
        frame_times = np.array(
            pd.read_csv(feature_file, delimiter=",", usecols=[1])['frameTime'])
        word_values = np.zeros((len(frame_times), MAX_LENGTH))
        check_next_word_array = np.zeros((len(frame_times),))
        tree = xml.etree.ElementTree.parse(annotation_file).getroot()
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

# NOTE: This is a creating a vocabulary and a mapping from the index to the tokens
# and vice versa and saving it to the different file formats.


def get_vocabulary_from_files(feature_files, annotations_dir, output_dir):
    # Collect corresponding annotation files for each feature file.
    collected_files = []
    for feature_file_path in feature_files:
        filename = os.path.splitext(os.path.basename(feature_file_path))[0]
        annotation_filename = "{}.timed-units.xml".format(filename)
        annotation_path = os.path.join(annotations_dir, annotation_filename)
        if os.path.isfile(annotation_path):
            collected_files.append((feature_file_path, annotation_path))
    words_from_annotations = []
    for feature_file, annotation_file in collected_files:
        tree = xml.etree.ElementTree.parse(annotation_file).getroot()
        for annotation_type in tree.findall('tu'):
            target_word = annotation_type.text.strip()
            if "--" in target_word:
                target_word = '--disfluency_token--'
                words_from_annotations.append(target_word)
            else:
                target_words = nltk.word_tokenize(target_word)
                words_from_annotations.extend(target_words)
    vocab = set(words_from_annotations)
    # +1 is because 0 represents no change
    word_to_ix = {word: i+1 for i, word in enumerate(vocab)}
    ix_to_word = {word_to_ix[wrd]: wrd for wrd in word_to_ix.keys()}
    with open(os.path.join(output_dir, "word_to_ix.p"), 'wb') as f:
        pickle.dump(word_to_ix, f)
    with open(os.path.join(output_dir, "ix_to_word.p"), 'wb') as f:
        pickle.dump(ix_to_word, f)
    with open(os.path.join(output_dir, "word_to_ix.json"), 'w') as f:
        json.dump(word_to_ix, f, indent=4)

# NOTE: In the original file, this was being done by splitting the data by .f .g
# The audio file naming conventions in the corpus are xxxxx.g.csv or xxxxx.f.csv
# TODO: Figure out why the data is split using this convention.
# NOTE: Originally, the author is trying to apply this function to the f and
# g audio files separately.


def prepare_data_acoustics_from_files(annotation_files, features_files, output_dir):

    def find_max_len(df_list):
        max_len = 0
        for df in df_list:
            max_len = max(max_len, len(df))
        return max_len
    # Creating output dataset file
    out_dataset_file = h5py.File(
        "{}/gemaps_split.hdf5".format(output_dir), 'w')
    # Collect corresponding annotation files for each feature file.
    collected_files = []
    for annotation_file in annotation_files:
        annotation_filename = os.path.splitext(
            os.path.basename(annotation_file))[0]
        for gemap_file in features_files:
            gemap_filename = os.path.splitext(os.path.basename(gemap_file))[0]
            if annotation_filename == gemap_filename:
                collected_files.append((annotation_file, gemap_file))

    for annotation_file, feature_file in collected_files:
        filename = os.path.splitext(
            os.path.basename(annotation_file))[0]
        split_indices = []
        annotation_df = pd.read_csv(annotation_file, delimiter=",")
        feature_df = pd.read_csv(feature_file, delimiter=",")
        for frame_time in annotation_df["frameTimes"][1:]:
            split_indices.append(
                np.max(np.where(feature_df['frameTime'] < frame_time)) + 1)
        data_split_list = np.split(feature_df, split_indices)
        max_len = find_max_len(data_split_list)
        data_dict = {
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
            data_output = {filename: data_dict}
            out_dataset_file.create_dataset(
                "{}/{}/{}".format(filename, 'x', feature_name),
                data=np.array(data_dict['x'][feature_name])
            )
            out_dataset_file.create_dataset(
                "{}/{}/{}".format(filename, 'x_i', feature_name),
                data=np.array(data_dict['x_i'][feature_name])
            )
    out_dataset_file.close()


def process_gemaps_from_files(feature_file_paths, output_dir):
    # Create dirs
    raw_features_dir = os.path.join(output_dir, "raw")
    z_normalized_dir = os.path.join(output_dir, "z_normalized")
    z_normalized_pooled_dir = os.path.join(output_dir, "z_normalized_pooled")
    os.makedirs(raw_features_dir)
    os.makedirs(z_normalized_dir)
    os.makedirs(z_normalized_pooled_dir)
    # Process all files
    for feature_file_path in feature_file_paths:
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


def extract_voice_activity_labels(feature_file_paths, annotations_dir, output_dir):
    # Check dirs
    assert os.path.isdir(output_dir)
    # Minimum size of a detection for potential voice activity.
    MINIMUM_DETECTION_MS = 0.025
    # Collect corresponding annotation files for each feature file.
    collected_files = []
    for feature_file_path in feature_file_paths:
        filename = os.path.splitext(os.path.basename(feature_file_path))[0]
        annotation_filename = "{}.timed-units.xml".format(filename)
        annotation_path = os.path.join(annotations_dir, annotation_filename)
        if os.path.isfile(annotation_path):
            collected_files.append((feature_file_path, annotation_path))
    pbar = tqdm(
        total=len(collected_files), desc="Extracting VAD")
    # Read all the file pairs and extract VA info.
    for feature_path, timed_unit_path in collected_files:
        frame_times = np.array(
            pd.read_csv(feature_path, delimiter=",", usecols=[1])['frameTime'])
        voice_activity = np.zeros((len(frame_times)))
        tree = xml.etree.ElementTree.parse(timed_unit_path).getroot()
        # Obtain the annotation data first.
        annotation_data = []
        for annotation_type in tree.findall('tu'):
            annotation_data.append(
                (float(annotation_type.get('start')),
                 float(annotation_type.get('end'))))
        # Remove any detections that are less than 90ms.
        # TODO: Determine why this is the case / why do this step.
        annotation_data = [data for data in annotation_data
                           if data[1] - data[0] >= MINIMUM_DETECTION_MS]
        # Only obtain the frames that contain voice activity for at least X%
        # of duration
        # TODO: Not sure how this is currently getting X% for VAD in frame.
        for start_frame, end_frame in annotation_data:
            start_idx = (np.abs(frame_times-start_frame)).argmin()
            end_idx = (np.abs(frame_times - end_frame)).argmin()
            voice_activity[start_idx: end_idx+1] = 1
        # Output the results
        output = pd.DataFrame([frame_times, voice_activity])
        output = np.transpose(output)
        output.columns = ['frameTimes', 'vad']
        filename = os.path.splitext(os.path.basename(feature_path))[0]
        output.to_csv(os.path.join(output_dir, "{}.csv".format(
            filename)), float_format='%.6f', sep=',', index=False, header=True)
        pbar.update(1)


def extract_gemaps_from_audio(
        audio_path, output_dir, opensmile_exe_path, config_path):
    assert os.path.isfile(audio_path)
    audio_name = os.path.splitext(os.path.basename(audio_path))[0]
    csv_path = os.path.join(output_dir, "{}.csv".format(audio_name))
    cmd = "{} -C {} -I {} -D {}".format(opensmile_exe_path, config_path,
                                        audio_path, csv_path)
    subprocess.run(cmd, shell=True)


def opensmile_py_extract_gemaps_from_audio(
        audio_path, output_dir, feature_set=opensmile.FeatureSet.GeMAPSv01b,
        feature_level=opensmile.FeatureLevel.Functionals, duration=None,
        num_workers=5):
    assert os.path.isfile(audio_path)
    if duration == None:
        signal, sampling_rate = audiofile.read(audio_path)
    else:
        assert duration > 0
        signal, sampling_rate = audiofile.read(audio_path, duration=duration)
    smile = opensmile.Smile(
        feature_set=feature_set,
        feature_level=feature_level,
        num_workers=num_workers)
    features = smile.process_signal(
        signal,
        sampling_rate)
    # Save to csv
    audio_name = os.path.splitext(os.path.basename(audio_path))[0]
    features.to_csv(os.path.join(output_dir, "{}.csv".format(audio_name)))
