# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-05-17 15:17:49
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-17 16:35:55

import argparse
import tqdm
import glob
import shutil
import subprocess
import os
from utils import *

# GLOBALS

ANNOTATIONS_URL = "http://groups.inf.ed.ac.uk/maptask/hcrcmaptask.nxtformatv2-1.zip"
DOWNLOAD_DIR_NAME = "maptask"


# ------------------------------ HELPER METHODS -------------------------

def get_annotations_from_url(output_dir : str) -> str:
    """
    Download the annotations and return a path to them.
    """
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    download_zip_from_url(ANNOTATIONS_URL, output_dir)
    return os.path.join(output_dir, os.listdir(output_dir)[0])

def get_audio_using_wget(output_dir : str) -> str:
    """
    Download the audio using the wget script from the maptask website and
    return a path to the audio data.
    NOTE: The wget script must be present in the same dir. as this script.
    """
    os.makedirs(output_dir,exist_ok=True)
    signals_dir_path = os.path.join(os.getcwd(),"signals")
    if os.path.isdir(signals_dir_path):
        shutil.rmtree(signals_dir_path)
    audio_wget_script_path = glob.glob("{}/maptaskBuild-*.sh".format(os.getcwd()))
    subprocess.run("chmod +x {}".format(audio_wget_script_path), shell=True)
    subprocess.run(audio_wget_script_path, shell=True)
    assert os.path.isdir(signals_dir_path)
    shutil.move(signals_dir_path,output_dir)
    assert os.path.join(output_dir,"signals")
    return os.path.join(output_dir,"signals")


def extract_mono_from_stereo(signals_dir : str, output_dir : str) -> str:
    """
    Extract mono audio from the stereo audio and return a path.
    """
    assert os.path.isdir(signals_dir)
    os.makedirs(output_dir,exist_ok=True)
    mono_dir_path = os.path.join(output_dir,"mono_signals")
    if os.path.isdir(mono_dir_path):
        shutil.rmtree(mono_dir_path)
    os.makedirs(mono_dir_path)
    stereo_paths = glob.glob("{}/*mix.wav".format(os.path.join(signals_dir,"dialogues")))
    pbar = tqdm(
        total=len(stereo_paths), desc="Extracting mono from stereo")
    for stereo_path in stereo_paths:
        stereo_to_mono(stereo_path, mono_dir_path)
        pbar.update(1)
    return mono_dir_path

# ------------------------------ MAIN METHODS ---------------------------

def download_full(output_dir : str) -> None:
    """
    Download the annotations and audio of the maptask corpus + extracts mono
    audio from the stereo audio for each speaker.
    """
    print("Downloading full corpus to: {}".format(output_dir))
    # Download annotations
    annotations_path = get_annotations_from_url(output_dir)
    # Download stereo
    signals_path = get_audio_using_wget(output_dir)
    # Extract mono
    mono_path = extract_mono_from_stereo(signals_path,output_dir)
    # Move the mono and stereo audio into the maptask data directory.
    maptask_data_dir = os.path.join(annotations_path,"Data")
    assert os.path.isdir(maptask_data_dir)
    shutil.move(mono_path,signals_path)
    shutil.move(signals_path,maptask_data_dir)

def download_annotations(output_dir : str) -> None:
    """
    Simply download the annotations of the maptask corpus
    """
    print("Downloading annotations to: {}".format(output_dir))
    # Download annotations
    get_annotations_from_url(output_dir)


def download_audio(output_dir : str) -> None:
    """
    Only download the audio of the maptask corpus and extract mono audio from
    the stereo.
    """
    print("Downloading audio to: {}".format(output_dir))
     # Download stereo
    signals_path = get_audio_using_wget(output_dir)
    # Extract mono
    extract_mono_from_stereo(signals_path,output_dir)


# Example command:  python download_maptask.py --out_dir ./test_full --full
if __name__ == "__main__":
    # Obtain args
    parser = argparse.ArgumentParser()
    parser.add_argument("--out_dir", dest="out_dir", type=str, required=True,
                        help="Path to the output directory")
    parser.add_argument("--full", dest="full", action="store_true",
            help="If set, download the annotations, stereo audio, and extract mono audio")
    parser.add_argument("--annotations", dest="annotations", action="store_true",
            help="If set, download the annotations only")
    parser.add_argument("--audio", dest="audio", action="store_true",
            help="If set, download the stereo and mono audio only")
    args = parser.parse_args()
    # Check dirs
    os.makedirs(args.out_dir,exist_ok=True)
    download_dir = os.path.join(args.out_dir,DOWNLOAD_DIR_NAME)
    if os.path.isdir(download_dir):
        shutil.rmtree(download_dir)
    os.makedirs(download_dir)
    # Check flags
    if args.full:
        download_full(download_dir)
    elif args.annotations:
        download_annotations(download_dir)
    elif args.audio:
        download_audio(download_dir)
    else:
        raise Exception("A download flag must be set")

