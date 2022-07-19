# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-11 16:58:36
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-19 16:19:30

import os
import requests
from tqdm import tqdm
from pathlib import Path
from pydub import AudioSegment
from zipfile import ZipFile
import shutil
import audiofile
from sklearn.model_selection import train_test_split
from data_pipelines.features.opensmile import OpenSmile

############################# GENERAL UTILS ################################

def reset_dir(dir_path):
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)

############################# DOWNLOAD UTILS ################################

def download_from_url(url, url_temp_path, chunk_size=8192):
    link_name = Path(url_temp_path).stem
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        pbar = tqdm(
            total=int(r.headers['Content-Length']), desc="{}".format(link_name))
        with open(url_temp_path, "wb+") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    pbar.update(len(chunk))


def download_zip_from_url(url, output_dir, extract=True, chunk_size=8192,
                          cleanup=True):
    link_name = Path(url).stem
    url_temp_path = "{}.zip".format(os.path.join(output_dir, link_name))
    # Download and extract
    download_from_url(url, url_temp_path, chunk_size)
    if extract:
        extract_from_zip(url_temp_path, output_dir)
    # Cleanup
    if cleanup:
        os.remove(url_temp_path)

def extract_from_zip(zip_file_path, output_dir):
    with ZipFile(zip_file_path, 'r') as zipObj:
        # Extract all the contents of zip file in different directory
        os.makedirs(output_dir, exist_ok=True)
        zipObj.extractall(output_dir)

######################## AUDIO MANIPULATION UTILS ##########################

def stereo_to_mono(stereo_path, output_dir,left_prefix="left",right_prefix="right"):
    """
    Split stereo file into two mono files.
    NOTE: Left channel is g and right channel is f.
    """
    assert os.path.isfile(stereo_path)
    ext = Path(stereo_path).suffix[1:]
    stereo_name = os.path.splitext(os.path.basename(stereo_path))[0]
    stereo_audio = AudioSegment.from_file(stereo_path, format=ext)
    mono_audios = stereo_audio.split_to_mono()
    basename = os.path.splitext(stereo_name)[0]
    left_path = os.path.join(output_dir, "{}.{}.{}".format(basename,left_prefix, ext))
    right_path = os.path.join(output_dir, "{}.{}.{}".format(basename, right_prefix, ext))
    mono_left = mono_audios[0].export(left_path, format=ext)
    mono_right = mono_audios[1].export(right_path, format=ext)
    return mono_left, mono_right


def extract_feature_set(audio_path, feature_set):
    signal, sampling_rate = audiofile.read(audio_path,always_2d=True)
    smile = OpenSmile(
        feature_set=feature_set,
        feature_level="lld",
        sample_rate=sampling_rate,
        normalize=False)
    f = smile(signal)
    return {
        "values" : f,
        "features" : list(smile.idx2feat.values())
    }


######################## DATASET UTILS ##########################

def get_train_val_test_splits(items, test_size, val_size,seed):
    """Generate train, val, test splits."""
    items = sorted(items)
    train_dialogues, test_dialogues = train_test_split(
        items, test_size=test_size,random_state=seed)
    train_dialogues, val_dialogues = train_test_split(
        items, test_size=val_size,random_state=seed)
    return train_dialogues, val_dialogues, test_dialogues