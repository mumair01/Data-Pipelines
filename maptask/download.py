# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-05-06 17:27:58
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-08 11:03:01

import os
import tensorflow_datasets as tfds
import argparse
from os import listdir, makedirs, system

# GLOBALS
ANNO_URL = "http://groups.inf.ed.ac.uk/maptask/hcrcmaptask.nxtformatv2-1.zip"
DIALOG_URL = "http://groups.inf.ed.ac.uk/maptask/signals/dialogues"


def download_dialogue(dataset_name, save_dir_path, url=None):
    if url == None:
        return
    download_path = "{}/{}".format(save_dir_path, "download")
    extract_path = "{}/{}".format(save_dir_path, "extract")
    [os.makedirs(path, exist_ok=True) for path in
     (save_dir_path, download_path, extract_path)]
    dl_manager = tfds.download.DownloadManager(
        download_dir=download_path,
        extract_dir=extract_path,
        dataset_name=dataset_name)
    dir_path = dl_manager.download_and_extract(url)
    return dir_path


def download_annotation(savepath, url=None):
    if url is None:
        url = ANNO_URL

    wget_cmd = ["wget", "-P", savepath, url, "-q", "--show-progress"]
    print("Downloading annotations")
    print("-----------------------")
    system(" ".join(wget_cmd))
    print("Download complete")

    print(f"Extracted annotations -> {savepath}/annotations")
    unzip_cmd = [
        "unzip",
        "-qq",
        os.path.join(savepath, "hcrcmaptask.nxtformatv2-1.zip"),
        "-d",
        savepath,
    ]
    system(" ".join(unzip_cmd))
    system(
        f'mv {os.path.join(savepath, "maptaskv2-1")} {os.path.join(savepath, "annotations")}')
    system(f'rm {os.path.join(savepath, "hcrcmaptask.nxtformatv2-1.zip")}')


def download_maptask(output_dir):
    """
    Download both the corpus and the annotations ans save to the output dir.
    """
    os.makedirs(output_dir, exist_ok=True)
    download_dialogue("maptask", output_dir, DIALOG_URL)
    download_annotation(output_dir, ANNO_URL)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out_dir", dest="out_dir", type=str, required=True,
                        help="Path to the output directory")
    args = parser.parse_args()
    download_maptask(args.out_dir)
