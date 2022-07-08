# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-05-17 16:19:15
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-08 13:31:24


import os
import subprocess
import opensmile
import audiofile
import argparse
import shutil
import glob


def extract_gemaps_from_maptask_audio(
        audio_dir_path, output_dir, config_path):
    """
    Read all the wav files from a directory and extract their features based on
    the given configurations.
    NOTE: Only .wav files are supported
    NOTE: opensmile must be downloaded and added to path : https://audeering.github.io/opensmile/get-started.html#default-feature-sets
    """
    assert os.path.isdir(audio_dir_path)
    os.makedirs(output_dir,exist_ok=True)
    assert os.path.isfile(config_path)
    config_name = os.path.splitext(os.path.basename(config_path))[0]
    # Read all wav files
    audio_paths = glob.glob("{}/*.wav".format(audio_dir_path))
    for audio_path in audio_paths:
        filename, ext = os.path.splitext(os.path.basename(audio_path))
        dialogue, participant = filename.split(".")
        if ext == ".wav":
            csv_path =os.path.join(output_dir,
                "{}.{}.{}.csv".format(dialogue,participant,config_name))
            cmd = "SMILExtract -C {} -I {} -D {}".format(
                config_path,audio_path,csv_path)
            subprocess.run(cmd, shell=True)

# Example command: python extract_audio_features.py --audio_dir maptask/mono_signals --out ./test --config config/custom/egemaps_v02_50ms/eGeMAPSv02.conf
if __name__ == "__main__":
    # Obtain args
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio_dir", dest="audio_dir", type=str,
                        help="Path to the input audio directory")
    parser.add_argument("--out", dest="out_dir", type=str, required=True,
                        help="Path to the output directory")
    parser.add_argument("--config", dest="config_path", type=str, required=True,
                        help="Path to the opensmile .conf file")
    args = parser.parse_args()
    extract_gemaps_from_maptask_audio(
        audio_dir_path = args.audio_dir,
        output_dir = args.out_dir,
        config_path = args.config_path
    )

