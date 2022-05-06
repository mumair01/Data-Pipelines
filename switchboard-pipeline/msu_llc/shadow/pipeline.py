# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-03-04 17:16:29
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-03-22 15:24:39

from typing import Dict
import sys
import os
import download
import preprocess_lc
import merge

# URLs
# Paths
PROJECT_ROOT_DIR = "."
DATASETS_ROOT_PATH = os.path.join(PROJECT_ROOT_DIR, "datasets")


def download_data():
    if not os.path.isdir(DATASETS_ROOT_PATH):
        os.makedirs(DATASETS_ROOT_PATH)
    ### -- DOWNLOAD
    corpus_download_map = {
        "msu-sb": download.download_msu,
        "lc-sb": download.download_lc
    }
    for dataset_name, func in corpus_download_map.items():
        results_dir = os.path.join(DATASETS_ROOT_PATH, dataset_name)
        if not os.path.isdir(results_dir):
            if func != None:
                func(results_dir)


def preprocess_corpora():
    preprocess_lc.re_utterize_lc_data(
        os.path.join(DATASETS_ROOT_PATH, "lc-sb"),
        os.path.join(DATASETS_ROOT_PATH, "lc-sb-utterized"))
    merge.merge_msu_lc_sb_corpora(
        os.path.join(DATASETS_ROOT_PATH, "lc-sb-utterized"),
        os.path.join(DATASETS_ROOT_PATH, "msu-sb"),
        os.path.join(DATASETS_ROOT_PATH, "msu_lc_merged"))


def run():
    # Download the data if needed
    download_data()
    # Preprocess the data
    preprocess_corpora()


if __name__ == "__main__":
    run()
