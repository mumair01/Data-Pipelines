# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-05-11 15:10:30
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-13 10:43:43

from threading import local
from typing import List
from multiprocessing import Pool
import os
import sys
import shutil
from pathlib import Path
from functools import partial
import h5py
import numpy as np
import pickle
import json
# Local
from corpus_scripts.maptask import MapTask
from feature_scripts.opensmile_features import extract_gemaps_from_audio
from feature_scripts.process_gemaps import process_gemaps_from_file
from feature_scripts.voice_activity_annotations import extract_voice_activity_labels
from feature_scripts.prepare_fast_feature_acoustics import prepare_data_acoustics_from_files
from feature_scripts.get_vocabulary import get_vocabulary_from_file
from feature_scripts.word_annotations import get_word_annotations_from_file
from feature_scripts.averaged_word_annotations import get_local_set_from_file, get_average_word_annotations_from_file
from decorators import *
from vardefs import *
from utils import *


class MapTaskPipelineSkantze:

    MAX_WORKERS = 10
    OPENSMILE_GEMAPS_CONFIG_PATHS = [GEMAPS_10SEC_CONFIG, GEMAPS_50SEC_CONFIG]
    # Partial output dir names
    GEMAPS_DIR_NAME = "gemaps"
    PROCESSED_GEMAPS_DIR_NAME = "processed_gemaps"
    EXTRACTED_VA_DIR_NAME = "voice_activity_annotations"
    FAST_ACOUSTIC_FEATURES_NAME = "fast_data_acoustics"
    VOCABULARY_NAME = "extracted_vocabulary"
    WORD_ANNOTATIONS_NAME = "word_advanced_annotations"
    AVERAGED_WORD_ANNOTATIONS = "word_advanced_annotations_averaged"

    def __init__(self, maptask: MapTask, num_workers: int = 5):
        assert 0 < num_workers < self.MAX_WORKERS
        self.maptask: MapTask = maptask
        self.num_workers = int(num_workers)
        self.thread_pool = Pool(num_workers)

    def run(self, output_dir: str, corpus_subset: float = 1.0):
        assert 0 < corpus_subset <= 1.0
        output_dir = os.path.join(output_dir, "maptask_processed")
        # reset_dir(output_dir) # TODO: Maybe this can be a parameter.
        for opensmile_config_path in self.OPENSMILE_GEMAPS_CONFIG_PATHS:
            self.__run_for_config(opensmile_config_path, output_dir)

    # -------------------------------- PRIVATE ---------------------------

    def __run_for_config(self, opensmile_config_path, output_dir):
        result_dir_path = os.path.join(output_dir, os.path.basename(
            Path(opensmile_config_path).parent))
        os.makedirs(result_dir_path, exist_ok=True)
        self.__extract_gemaps(opensmile_config_path, result_dir_path)
        self.__process_gemaps(result_dir_path)
        self.__extract_voice_activity_annotations(result_dir_path)
        self.__prepare_fast_data_acoustics(result_dir_path)
        self.__get_vocabulary(result_dir_path)
        self.__get_word_annotations(result_dir_path)
        self.__get_averaged_word_annotations(result_dir_path)

    @print_component_decorator
    def __extract_gemaps(self, opensmile_config_path, output_dir):
        assert os.path.isfile(opensmile_config_path)
        assert os.path.isdir(output_dir)
        output_dir = os.path.join(output_dir, self.GEMAPS_DIR_NAME)
        if os.path.isdir(output_dir):
            return
        os.makedirs(output_dir)
        # Extract from all stereo audio files
        audio_paths = self.maptask.get_mono_audio_paths(participant=None)
        func = partial(extract_gemaps_from_audio, output_dir=output_dir,
                       opensmile_exe_path=OPENSMILE_EXE_PATH, config_path=opensmile_config_path)
        self.thread_pool.map(func, audio_paths)

    @print_component_decorator
    def __process_gemaps(self, output_dir):
        gemaps_processed_dir = os.path.join(
            output_dir, self.PROCESSED_GEMAPS_DIR_NAME)
        if os.path.isdir(gemaps_processed_dir):
            return
        os.makedirs(gemaps_processed_dir, exist_ok=True)
        raw_gemaps_dir = os.path.join(output_dir, self.GEMAPS_DIR_NAME)
        assert os.path.isdir(raw_gemaps_dir)
        # Create three different output directories
        raw_features_dir = os.path.join(gemaps_processed_dir, "raw")
        z_normalized_dir = os.path.join(gemaps_processed_dir, "z_normalized")
        z_normalized_pooled_dir = os.path.join(
            gemaps_processed_dir, "z_normalized_pooled")
        os.makedirs(raw_features_dir)
        os.makedirs(z_normalized_dir)
        os.makedirs(z_normalized_pooled_dir)
        # Read the feature files
        feature_file_paths = get_paths_from_directory(
            raw_gemaps_dir, files=True, ext=".csv")
        # Process per file
        func = partial(process_gemaps_from_file,
                       raw_features_dir=raw_features_dir,
                       z_normalized_dir=z_normalized_dir,
                       z_normalized_pooled_dir=z_normalized_pooled_dir)
        self.thread_pool.map(func, feature_file_paths)

    @print_component_decorator
    def __extract_voice_activity_annotations(self, output_dir):
        va_annotations_dir = os.path.join(
            output_dir, self.EXTRACTED_VA_DIR_NAME)
        if os.path.isdir(va_annotations_dir):
            # shutil.rmtree(va_annotations_dir)
            return
        os.makedirs(va_annotations_dir)
        # Get the raw gemaps and time-units files and collect them
        raw_gemaps_dir = os.path.join(output_dir, self.GEMAPS_DIR_NAME)
        assert os.path.isdir(raw_gemaps_dir)
        feature_file_paths = get_paths_from_directory(
            raw_gemaps_dir, files=True, ext=".csv")
        timed_unit_paths = self.maptask.get_timed_units()
        collected = self.__collect_csv_and_timed_unit_paths(
            feature_file_paths, timed_unit_paths)
        func = partial(
            extract_voice_activity_labels, output_dir=va_annotations_dir)
        self.thread_pool.starmap(func, collected)

    @print_component_decorator
    def __prepare_fast_data_acoustics(self, output_dir):
        assert os.path.isdir(output_dir)
        fast_data_acoustics_dir = os.path.join(
            output_dir, self.FAST_ACOUSTIC_FEATURES_NAME)
        if os.path.isdir(fast_data_acoustics_dir):
            return
            # shutil.rmtree(fast_data_acoustics_dir)
        os.makedirs(fast_data_acoustics_dir)
        # Need the voice activity and raw gemaps collected together.
        raw_gemaps_dir = os.path.join(output_dir, self.GEMAPS_DIR_NAME)
        assert os.path.isdir(raw_gemaps_dir)
        feature_file_paths = get_paths_from_directory(
            raw_gemaps_dir, files=True, ext=".csv")
        va_annotations_dir = os.path.join(
            output_dir, self.EXTRACTED_VA_DIR_NAME)
        assert os.path.isdir(va_annotations_dir)
        va_annotation_file_paths = get_paths_from_directory(
            va_annotations_dir, files=True, ext=".csv")
        collected = self.__collected_csv_csv_paths(
            va_annotation_file_paths, feature_file_paths)
        # Create h5 file for all datasets
        h5_f = h5py.File(
            "{}/gemaps_split.hdf5".format(fast_data_acoustics_dir), 'w')
        data_dicts = self.thread_pool.starmap(
            prepare_data_acoustics_from_files, collected)
        for data_dict in data_dicts:
            filename = data_dict['filename']
            for feature_name in GEMAP_FULL_FEATURES:
                h5_f.create_dataset(
                    "{}/{}/{}".format(filename, 'x', feature_name),
                    data=np.array(data_dict['x'][feature_name])
                )
                h5_f.create_dataset(
                    "{}/{}/{}".format(filename, 'x_i', feature_name),
                    data=np.array(data_dict['x_i'][feature_name]))
        h5_f.close()

    @print_component_decorator
    def __get_vocabulary(self, output_dir):
        assert os.path.isdir(output_dir)
        vocab_dir = os.path.join(output_dir, self.VOCABULARY_NAME)
        if os.path.isdir(vocab_dir):
            return
            # shutil.rmtree(vocab_dir)
        os.makedirs(vocab_dir)
        # This needs to be done for all types of processed gemaps
        # NOTE: Only doing for the znormalizedpool results rn.
        z_normalized_pooled_dir = os.path.join(
            output_dir, self.PROCESSED_GEMAPS_DIR_NAME, "z_normalized_pooled")
        assert os.path.isdir(z_normalized_pooled_dir)
        z_normalized_pool_paths = get_paths_from_directory(
            z_normalized_pooled_dir, files=True, ext=".csv")
        # Read the timed units once
        timed_unit_paths = self.maptask.get_timed_units()
        # Collect all the files
        collected = self.__collect_csv_and_timed_unit_paths(
            z_normalized_pool_paths, timed_unit_paths)
        words_from_annotation_lists = self.thread_pool.starmap(
            get_vocabulary_from_file, collected)
        vocab = set().union(*words_from_annotation_lists)
        # +1 is because 0 represents no change
        word_to_ix = {word: i+1 for i, word in enumerate(vocab)}
        ix_to_word = {word_to_ix[wrd]: wrd for wrd in word_to_ix.keys()}
        with open(os.path.join(vocab_dir, "word_to_ix.p"), 'wb') as f:
            pickle.dump(word_to_ix, f)
        with open(os.path.join(vocab_dir, "ix_to_word.p"), 'wb') as f:
            pickle.dump(ix_to_word, f)
        with open(os.path.join(vocab_dir, "word_to_ix.json"), 'w') as f:
            json.dump(word_to_ix, f, indent=4)

    @print_component_decorator
    def __get_word_annotations(self, output_dir):
        assert os.path.isdir(output_dir)
        word_annotations_dir = os.path.join(
            output_dir, self.WORD_ANNOTATIONS_NAME)
        if os.path.isdir(word_annotations_dir):
            return
            # shutil.rmtree(word_annotations_dir)
        os.makedirs(word_annotations_dir)
        # This needs to be done for all types of processed gemaps
        # NOTE: Only doing for the znormalizedpool results rn.
        z_normalized_pooled_dir = os.path.join(
            output_dir, self.PROCESSED_GEMAPS_DIR_NAME, "z_normalized_pooled")
        assert os.path.isdir(z_normalized_pooled_dir)
        z_normalized_pool_paths = get_paths_from_directory(
            z_normalized_pooled_dir, files=True, ext=".csv")
        # Read the timed units once
        timed_unit_paths = self.maptask.get_timed_units()
        word_to_ix_path = os.path.join(
            output_dir, self.VOCABULARY_NAME, "word_to_ix.p")
        assert os.path.isfile(word_to_ix_path)
        word_to_ix = pickle.load(open(word_to_ix_path, 'rb'))
        # Collect all the files
        collected = self.__collect_csv_and_timed_unit_paths(
            z_normalized_pool_paths, timed_unit_paths)
        func = partial(
            get_word_annotations_from_file, output_dir=word_annotations_dir,
            word_to_ix=word_to_ix)
        self.thread_pool.starmap(func, collected)

    @print_component_decorator
    def __get_averaged_word_annotations(self, output_dir):
        assert os.path.isdir(output_dir)
        avg_word_annotations_dir = os.path.join(
            output_dir, self.AVERAGED_WORD_ANNOTATIONS)
        if os.path.isdir(avg_word_annotations_dir):
            return
            # shutil.rmtree(avg_word_annotations_dir)
        os.makedirs(avg_word_annotations_dir)
        # This needs to be done for all types of processed gemaps
        # NOTE: Only doing for the znormalizedpool results rn.
        z_normalized_pooled_dir = os.path.join(
            output_dir, self.PROCESSED_GEMAPS_DIR_NAME, "z_normalized_pooled")
        assert os.path.isdir(z_normalized_pooled_dir)
        z_normalized_pool_paths = get_paths_from_directory(
            z_normalized_pooled_dir, files=True, ext=".csv")
        # Need the word annotations
        word_annotations_dir = os.path.join(
            output_dir, self.WORD_ANNOTATIONS_NAME)
        assert os.path.isdir(word_annotations_dir)
        word_annotation_paths = get_paths_from_directory(
            word_annotations_dir, files=True, ext=".csv")
        local_set_list = self.thread_pool.map(
            get_local_set_from_file, word_annotation_paths)
        total_set = set().union(*local_set_list)
        func = partial(
            get_average_word_annotations_from_file, total_set=total_set,
            output_dir=avg_word_annotations_dir)
        #  Collect the files
        collected = self.__collected_csv_csv_paths(
            z_normalized_pool_paths, word_annotation_paths)
        self.thread_pool.starmap(func, collected)

        #  -- Others

    def __collected_csv_csv_paths(self, csv1_paths, csv2_paths):
        collected = []
        for path1 in csv1_paths:
            csv1_name = get_filename_from_path(path1)
            for path2 in csv2_paths:
                csv2_name = get_filename_from_path(path2)
                if csv1_name == csv2_name:
                    collected.append((path1, path2))
        return collected

    def __collect_csv_and_timed_unit_paths(self, csv_paths, timed_unit_paths):
        collected = []
        for path in csv_paths:
            csv_name = get_filename_from_path(path)
            for timed_unit_path in timed_unit_paths:
                timed_unit_name = get_filename_from_path(timed_unit_path)
                timed_unit_name = timed_unit_name[:timed_unit_name.find(".")+2]
                if csv_name == timed_unit_name:
                    collected.append((path, timed_unit_path))
        return collected
