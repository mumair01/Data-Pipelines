# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-05-06 17:27:58
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-11 14:04:59

# Standard imports
import os
import argparse
from pyexpat import features
import shutil
import subprocess
import glob
from pathlib import Path
from tqdm import tqdm
from vardefs import *
from utils import *
from process import *


def download_maptask(download_dir, overwrite=False):
    #  Check dirs.
    if os.path.isdir(download_dir):
        if overwrite:
            shutil.rmtree(download_dir)
        else:
            return
    os.makedirs(download_dir)
    # Download annotations
    download_zip_from_url(ANNOTATIONS_URL, download_dir)
    # ---- Download audio
    # Check paths exist
    maptask_data_dir_path = os.path.join(
        download_dir, os.listdir(download_dir)[0], "Data")
    signals_dir_name = "signals"
    signals_dir_local_path = os.path.join(SCRIPTS_PATH, signals_dir_name)
    signals_dir_maptask_path = os.path.join(
        maptask_data_dir_path, signals_dir_name)
    assert os.path.isdir(maptask_data_dir_path)
    # NOTE: Shell should be in Project root - this will create a signals dir in root.
    if not os.path.isdir(signals_dir_local_path) and not os.path.isdir(
            signals_dir_maptask_path):
        subprocess.run(
            "chmod +x {}".format(AUDIO_WGET_SCRIPT_PATH), shell=True)
        subprocess.run(AUDIO_WGET_SCRIPT_PATH, shell=True)
    if os.path.isdir(signals_dir_local_path):
        shutil.move(signals_dir_local_path, maptask_data_dir_path)
    assert os.path.isdir(signals_dir_maptask_path)


def maptask_stereo_to_mono(download_dir, overwrite=False):
    # Check dirs
    maptask_signals_dir_path = os.path.join(
        download_dir, os.listdir(download_dir)[0], "Data/signals")
    stereo_dir = os.path.join(maptask_signals_dir_path, "dialogues")
    mono_dir = os.path.join(maptask_signals_dir_path, "mono_dialogues")
    # Do not proceed if dir exists
    if os.path.isdir(mono_dir) and not overwrite:
        return
    if overwrite:
        shutil.rmtree(mono_dir)
    assert os.path.isdir(download_dir)
    assert os.path.isdir(stereo_dir)
    os.makedirs(mono_dir, exist_ok=True)
    # Convert all the stereo files into mono
    # NOTE: Audio ext. is wav for original data. See: https://groups.inf.ed.ac.uk/maptask/maptasknxt.html
    stereo_paths = glob.glob("{}/*mix.wav".format(stereo_dir))
    pbar = tqdm(
        total=len(stereo_paths), desc="Extracting mono from stereo")
    for stereo_path in stereo_paths:
        stereo_to_mono(stereo_path, mono_dir)
        pbar.update(1)


def extract_gemaps(audio_files, output_dir, subset=1.0, overwrite=False):
    if os.path.isdir(output_dir) and not overwrite:
        return
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
    # Create the output dirs.
    os.makedirs(output_dir)
    # TODO: Need to add functionality for getting features from different frames.
    #  Extract Features
    # NOTE: Right now, this is producing frameSize 20 ms with stepSize 10 ms.
    # Get a subset of the files
    gemaps_extract_dir = os.path.join(output_dir, "gemaps_extract_20ms")
    os.makedirs(gemaps_extract_dir)
    subset_len = int((subset * len(audio_files)))
    pbar = tqdm(
        total=subset_len, desc="Extracting Audio Features")
    for mono_file in audio_files[:subset_len]:
        extract_gemaps_from_audio(
            audio_path=mono_file,
            output_dir=gemaps_extract_dir,
            opensmile_exe_path=OPENSMILE_EXE_PATH,
            config_path=GEMAPS_50SEC_CONFIG)
        pbar.update(1)


def process_gemaps(gemaps_dir_path, processed_dir, overwrite=False):
    # Check dirs
    assert os.path.isdir(gemaps_dir_path)
    assert os.path.isdir(processed_dir)
    gemap_processed_dir_path = os.path.join(
        processed_dir, "{}_processed".format(os.path.basename(gemaps_dir_path)))
    if os.path.isdir(gemap_processed_dir_path) and not overwrite:
        return
    if os.path.isdir(gemap_processed_dir_path):
        shutil.rmtree(gemap_processed_dir_path)
    os.makedirs(gemap_processed_dir_path)
    # Get the gemaps dirs
    # NOTE: Assuming that there are sub-directories in the gemaps folder.
    gemap_dirs = glob.glob("{}/**".format(gemaps_dir_path))
    # Read all the gemaps files
    # TODO: This should process all the gemap directories when they exist.
    raw_gemap_paths = glob.glob("{}/*.csv".format(gemap_dirs[0]))
    process_gemaps_from_files(raw_gemap_paths, gemap_processed_dir_path)


def extract_voice_activity_annotations(
        download_dir, processed_dir,  gemaps_dir_path, overwrite=False):
    # Check and create dirs
    assert os.path.isdir(download_dir)
    assert os.path.isdir(processed_dir)
    assert os.path.isdir(gemaps_dir_path)
    timed_units_dir = os.path.join(
        download_dir, os.listdir(download_dir)[0], "Data/timed-units")
    assert os.path.isdir(timed_units_dir)
    annotations_dir = os.path.join(processed_dir, "voice_activity_annotations")
    if os.path.isdir(annotations_dir) and not overwrite:
        return
    if os.path.isdir(annotations_dir):
        shutil.rmtree(annotations_dir)
    os.makedirs(annotations_dir)
    # gemaps will contain different dirs for different gemap settings. Ex: 20ms frame size
    gemap_dirs = [os.path.join(gemaps_dir_path, gemap_dir)
                  for gemap_dir in os.listdir(gemaps_dir_path)]
    for gemap_dir in gemap_dirs:
        features_files = glob.glob("{}/*.csv".format(gemap_dir))
        extract_voice_activity_labels(
            features_files, timed_units_dir, annotations_dir)


def prepare_fast_data_acoustics(processed_dir, gemaps_dir_path, overwrite=False):
    # Check and create dirs.
    assert os.path.isdir(processed_dir)
    assert os.path.isdir(gemaps_dir_path)
    annotations_dir = os.path.join(processed_dir, "voice_activity_annotations")
    assert os.path.isdir(annotations_dir)
    # TODO: Give the output directory a more reasonable name later on.
    fast_data_acoustics_dir = os.path.join(
        processed_dir, "fast_data_acoustics")
    if os.path.isdir(fast_data_acoustics_dir) and not overwrite:
        return
    if os.path.isdir(fast_data_acoustics_dir):
        shutil.rmtree(fast_data_acoustics_dir)
    os.makedirs(fast_data_acoustics_dir)
    annotation_files = glob.glob("{}/*.csv".format(annotations_dir))
    gemap_dirs = [os.path.join(gemaps_dir_path, gemap_dir)
                  for gemap_dir in os.listdir(gemaps_dir_path)]
    # TODO: There may be many gemaps dirs - right now we're only choosing the
    # first one to make sure the pipeline works but this should be supported
    # later.
    # Load gemap files
    # NOTE: Doing idx 1 because first is .DS_Store - annoying.
    features_files = glob.glob("{}/*.csv".format(gemap_dirs[1]))
    prepare_data_acoustics_from_files(
        annotation_files, features_files, fast_data_acoustics_dir)


def get_vocabulary(download_dir, processed_dir, overwrite=False):
    assert os.path.isdir(processed_dir)
    output_dir = os.path.join(processed_dir, "extracted_annotations")
    if os.path.isdir(output_dir) and not overwrite:
        return
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    # This process needs the processed gemap features
    # NOTE: This should be done for all - but simply doing it for one processed
    # dir right now.
    processed_gemaps_dir = os.path.join(
        processed_dir, "gemaps_processed/z_normalized")
    assert os.path.isdir(processed_gemaps_dir)
    processed_feature_files = glob.glob(
        "{}/*.csv".format(processed_gemaps_dir))
    # Also needs the timed annotations - this comes from the original data
    timed_units_dir = os.path.join(
        download_dir, os.listdir(download_dir)[0], "Data/timed-units")
    # Process
    get_vocabulary_from_files(processed_feature_files,
                              timed_units_dir, output_dir)


def get_word_annotations(download_dir, processed_dir, overwrite=False):
    assert os.path.isdir(processed_dir)
    output_dir = os.path.join(processed_dir, "word_advanced_annotations")
    if os.path.isdir(output_dir) and not overwrite:
        return
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    # This process needs the processed gemap features
    # NOTE: This should be done for all - but simply doing it for one processed
    # dir right now.
    processed_gemaps_dir = os.path.join(
        processed_dir, "gemaps_processed/z_normalized")
    assert os.path.isdir(processed_gemaps_dir)
    processed_feature_files = glob.glob(
        "{}/*.csv".format(processed_gemaps_dir))
    # Also needs the timed annotations - this comes from the original data
    timed_units_dir = os.path.join(
        download_dir, os.listdir(download_dir)[0], "Data/timed-units")
    # This also needs the vocabulary.
    word_to_ix = pickle.load(open(
        os.path.join(processed_dir, "extracted_annotations", "word_to_ix.p"), 'rb'))
    get_word_annotations_from_files(
        processed_feature_files, timed_units_dir, word_to_ix, output_dir)


def get_averaged_word_annotations(download_dir, processed_dir, overwrite=False):
    assert os.path.isdir(processed_dir)
    output_dir = os.path.join(
        processed_dir, "word_advanced_annotations_averaged")
    if os.path.isdir(output_dir) and not overwrite:
        return
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    # This process needs the processed gemap features
    # NOTE: This should be done for all - but simply doing it for one processed
    # dir right now.
    processed_gemaps_dir = os.path.join(
        processed_dir, "gemaps_processed/z_normalized")
    assert os.path.isdir(processed_gemaps_dir)
    processed_feature_files = glob.glob(
        "{}/*.csv".format(processed_gemaps_dir))
    # This also needs the vocabulary.
    word_to_ix = pickle.load(open(
        os.path.join(processed_dir, "extracted_annotations", "word_to_ix.p"), 'rb'))
    # Need the original word annotations
    word_annotation_dir = os.path.join(
        processed_dir, "word_advanced_annotations")
    get_average_word_annotations_from_file(
        processed_feature_files, word_annotation_dir, word_to_ix, output_dir)

# NOTE: Maybe subset / proportion of the corpus to process should be a param here.


def process_maptask(download_dir, processed_dir, overwrite=False):
    if os.path.isdir(processed_dir) and overwrite:
        shutil.rmtree(processed_dir)
    os.makedirs(processed_dir, exist_ok=True)
    # Generate paths
    maptask_signals_dir_path = os.path.join(
        download_dir, os.listdir(download_dir)[0], "Data/signals")
    mono_dir = os.path.join(maptask_signals_dir_path, "mono_dialogues")
    assert os.path.isdir(mono_dir)
    # Extract the gemaps features
    gemaps_dir_path = os.path.join(processed_dir, "gemaps")
    extract_gemaps(
        audio_files=[os.path.join(mono_dir, file)
                     for file in os.listdir(mono_dir)],
        output_dir=gemaps_dir_path,
        subset=0.01,
        overwrite=False)
    # Prepare the gemap features
    process_gemaps(
        gemaps_dir_path, processed_dir, overwrite=False)
    # Extract voice activity annotations
    extract_voice_activity_annotations(
        download_dir, processed_dir, gemaps_dir_path, overwrite=False)
    # Prepare fast data acoustic features
    prepare_fast_data_acoustics(
        processed_dir, gemaps_dir_path, overwrite=False)
    # Get the vocabulary
    get_vocabulary(download_dir, processed_dir, overwrite=False)
    #  Get word annotations
    get_word_annotations(download_dir, processed_dir, overwrite=False)
    # Get the averaged word annotations
    get_averaged_word_annotations(download_dir, processed_dir, overwrite=True)

# TODO: Right now, the pipeline does not know about how the gemap features
# are extracted e.g., 10ms or 50 ms or whatever.
# At some point, this should be configurable so that the directory paths
# are clear.


def pipeline(output_dir):
    # Create the appropriate directories
    maptask_dir = os.path.join(output_dir, DATASET_NAME)
    download_dir = os.path.join(maptask_dir, "download")  # Raw download dir.
    processed_dir = os.path.join(maptask_dir, "processed")  # Processed dir.
    os.makedirs(output_dir, exist_ok=True)
    # Download
    download_maptask(download_dir, overwrite=False)
    maptask_stereo_to_mono(download_dir, overwrite=False)
    #
    process_maptask(download_dir, processed_dir, overwrite=False)


# GLOBAL
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out_dir", dest="out_dir", type=str, required=True,
                        help="Path to the output directory")
    args = parser.parse_args()
    pipeline(args.out_dir)
