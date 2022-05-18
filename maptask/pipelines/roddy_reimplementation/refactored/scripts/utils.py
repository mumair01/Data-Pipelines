# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-05-11 14:52:38
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-13 10:01:01

'''
Contains general methods that might be useful across pipelines.
'''

import os
import shutil
import requests
from tqdm import tqdm
from pathlib import Path
from pydub import AudioSegment
import numpy as np
from zipfile import ZipFile


def find_nearest(array, value):
    idx = (np.abs(array-value)).argmin()
    return idx


def find_max_len(df_list):
    """
    Max length of a  dataframe from list of dataframes
    """
    max_len = 0
    for df in df_list:
        max_len = max(max_len, len(df))
    return max_len


def reset_dir(dir_path):
    """
    Remove and create new dir with same name if it exists
    """
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)


def get_filename_from_path(file_path):
    assert os.path.isfile(file_path)
    return os.path.splitext(os.path.basename(file_path))[0]


def get_file_ext_from_path(file_path):
    assert os.path.isfile(file_path)
    return os.path.splitext(os.path.basename(file_path))[1]


def get_parent_dir_from_path(path):
    return Path(path).parent


def get_paths_from_directory(dir_path, files=False, subdirs=False, ext=None):
    abs_file_paths = []
    abs_dir_paths = []
    for root, dirs, files in os.walk(os.path.abspath(dir_path)):
        for file in files:
            if ext == None:
                abs_file_paths.append(os.path.join(root, file))
            elif os.path.splitext(file)[1] == ext:
                abs_file_paths.append(os.path.join(root, file))
        for directory in dirs:
            abs_dir_paths.append(os.path.join(root, directory))
        break
    if files and subdirs:
        paths = []
        paths.extend(abs_file_paths)
        paths.extend(abs_dir_paths)
        return paths
    if files:
        return abs_file_paths
    if subdirs:
        return abs_dir_paths


def stereo_to_mono(stereo_path, output_dir):
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
    mono_left = mono_audios[0].export(
        os.path.join(output_dir, "{}.g.{}".format(basename, ext)), format=ext)
    mono_right = mono_audios[1].export(
        os.path.join(output_dir, "{}.f.{}".format(basename, ext)), format=ext)


def download_from_url(url, url_temp_path, chunk_size):
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
