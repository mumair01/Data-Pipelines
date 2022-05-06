# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-03-04 17:34:04
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-03-17 10:07:13
import sys
import os
from utils import *
from tqdm import tqdm


def download_dataset(url, name, result_dir):
    download_dir = os.path.join(result_dir, "download")
    extract_dir = os.path.join(result_dir, "extracted")

    print("{}: Downloading...".format(name))
    download_path = download_from_url(
        url, download_dir, extract_dir, name)
    print("{}: Downloaded to --> {}".format(name, download_path))
    print("{}: Extracted to --> {}".format(name, extract_dir))
    return download_path, extract_dir


def download_msu(result_dir):

    # Constants
    MSU_SB_URL = "https://us.openslr.org/resources/5/switchboard_word_alignments.tar.gz"
    MSU_SB_NAME = "msu_switchboard"
    _, extract_dir = download_dataset(
        MSU_SB_URL, MSU_SB_NAME, result_dir)
    msu_data_path = os.path.join(
        extract_dir, os.listdir(extract_dir)[0])
    print(msu_data_path)
    for root, dirs, files in tqdm(os.walk(msu_data_path)):
        for file in files:
            shutil.move(os.path.join(root, file), result_dir)
    print("{}: Data directory --> {}".format(MSU_SB_NAME, result_dir))
    return result_dir


def download_lc(result_dir):
    LC_SB_URL = "https://web.stanford.edu/~jurafsky/swb1_dialogact_annot.tar.gz"
    LC_SB_NAME = "lc_switchboard"
    _, extract_dir = download_dataset(
        LC_SB_URL, LC_SB_NAME, result_dir)
    lc_data_path = os.path.join(
        extract_dir, os.listdir(extract_dir)[0])
    for root, dirs, files in tqdm(os.walk(lc_data_path)):
        for file in files:
            shutil.move(os.path.join(root, file), result_dir)
    print("{}: Data directory --> {}".format(LC_SB_NAME, result_dir))
    return result_dir
