# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-11 16:58:36
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-21 15:48:00

import os
import sys
import requests
from tqdm import tqdm
from pathlib import Path
from pydub import AudioSegment
from zipfile import ZipFile
import shutil
import audiofile
from sklearn.model_selection import train_test_split
import json
import subprocess

from data_pipelines.features.opensmile import OpenSmile
from data_pipelines.utils import get_module_path

############################# GLOBALS #####################################

if sys.platform == "darwin":
    # NOTE: This is the MAC OSX compiled binary for shp2pipe
    SPH2PIPE_EXE_PATH = os.path.join(get_module_path(), "bin","sph2pipe_osx")
elif sys.platform == "linux":
    SPH2PIPE_EXE_PATH = os.path.join(get_module_path(), "bin","sph2pipe")


############################# GENERAL UTILS ################################

def reset_dir(dir_path):
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)

def write_json(data, filename):
    with open(filename, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False)


def read_json(path, encoding="utf8"):
    with open(path, "r", encoding=encoding) as f:
        data = json.loads(f.read())
    return data

def write_txt(txt, name):
    with open(name, "w") as f:
        f.write("\n".join(txt))


def read_txt(path, encoding="utf-8"):
    data = []
    with open(path, "r", encoding=encoding) as f:
        for line in f.readlines():
            data.append(line.strip())
    return data

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


# TODO: Add the other sph2pipe flags.
def sph2pipe(infile, outdir=None,outfile_suffix="", c=None):
    """Python wrapper for sph2pipe tool"""
    assert os.path.isfile(infile)
    # Generate the outfile path
    if outdir == None:
        outfile = infile.replace(".sph",f".wav")
    else:
        assert os.path.isdir(outdir)
        outfile = os.path.join(
            outdir, os.path.basename(infile).replace(".sph",f".wav"))
    # Add the outfile suffix
    name, ext = os.path.splitext(os.path.basename(outfile))
    outfile = os.path.join(os.path.dirname(outfile),f"{name}{outfile_suffix}.{ext[1:]}")
    # Does not process if the outfile exists
    if not os.path.isfile(outfile):
        # Construct the arguments
        args = [SPH2PIPE_EXE_PATH]
        if c != None:
            args.extend(["-c", str(c)])
        args.extend([infile,outfile])
        # Call the process
        subprocess.check_call(args)
    return outfile

######################## DATASET UTILS ##########################

def get_train_val_test_splits(items, test_size, val_size,seed):
    """Generate train, val, test splits."""
    items = sorted(items)
    train_dialogues, test_dialogues = train_test_split(
        items, test_size=test_size,random_state=seed)
    train_dialogues, val_dialogues = train_test_split(
        items, test_size=val_size,random_state=seed)
    return train_dialogues, val_dialogues, test_dialogues
