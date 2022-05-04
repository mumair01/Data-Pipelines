# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-03-04 17:17:38
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-03-05 11:51:42

import os
import tensorflow_datasets as tfds
import shutil
import pathlib


def download_from_url(url, download_dir, extract_dir, dataset_name, unzip=True):
    if os.path.isdir(download_dir):
        return
    os.makedirs(download_dir)
    os.makedirs(extract_dir, exist_ok=True)
    dl_manager = tfds.download.DownloadManager(
        download_dir=download_dir,
        extract_dir=extract_dir,
        dataset_name=dataset_name)
    if unzip:
        return dl_manager.download_and_extract(url)
    else:
        return dl_manager.download(url)


def get_files_with_ext(base_dir, ext, check_subdirs=True):
    paths = []
    if check_subdirs:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if ext in file:
                    paths.append(os.path.join(root, file))
    else:
        paths = [os.path.join(base_dir, x)
                 for x in os.listdir(base_dir) if ext in x]
    return paths
