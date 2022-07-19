# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-03-04 17:16:29
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-06 17:15:44

# Standard imports
import argparse
from typing import Dict
import sys
import os
import shutil
# Local imports
import download
import preprocess_lc
import merge

DATASET_NAME = "MSU_LLC_switchboard"


#  -----
def download_data(output_dir):
    """
    Download the MSU and LLC data.
    """
    ### -- DOWNLOAD
    corpus_download_map = {
        "msu-sb": download.download_msu,
        "lc-sb": download.download_lc
    }
    for dataset_name, func in corpus_download_map.items():
        results_dir = os.path.join(output_dir, dataset_name)
        if not os.path.isdir(results_dir):
            if func != None:
                func(results_dir)


def run_msu_llc_switchbord_pipeline(dataset_name, output_dir):
    """
    Download switchboard transcriptions from MSU and LLC SwDA, merge the
    transcripts, and process the data.
    """
    # Create dirs
    print("Initializing output directory: {}...".format(output_dir))
    os.makedirs(output_dir, exist_ok=True)
    result_path = os.path.join(output_dir, dataset_name)
    if os.path.isdir(result_path):
        shutil.rmtree(result_path)
    os.makedirs(result_path)
    # Download all the switchboard transcriptions
    print("Downloading data...")
    download_data(result_path)
    # Preprocess: Re-utterize the LC data
    print("Re-utterizing lc-sb data...")
    preprocess_lc.re_utterize_lc_data(
        os.path.join(output_dir, "lc-sb"),
        os.path.join(output_dir, "lc-sb-utterized"))
    # Merge the utterized lc data and the msu data
    # print("Merging MSU and LC transcriptions...")
    # merge.merge_msu_lc_sb_corpora(
    #     os.path.join(output_dir, "lc-sb-utterized"),
    #     os.path.join(output_dir, "msu-sb"),
    #     os.path.join(output_dir, "msu_lc_merged"))
    # Map the dialogue act tags

    # Add FTOs to the data

    # Prepare the data in different file formats.
    print("Data generated to: {}".format(output_dir))


if __name__ == "__main__":
    # Obtain args
    parser = argparse.ArgumentParser()
    parser.add_argument("--out_dir", dest="out_dir", type=str, required=True,
                        help="Path to the output directory")
    args = parser.parse_args()

    run_msu_llc_switchbord_pipeline(
        dataset_name=DATASET_NAME,
        output_dir=args.out_dir
    )
