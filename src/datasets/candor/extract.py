# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-04-10 11:15:43
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-04-10 11:37:30

import argparse
import os
import sys
import shutil
from tqdm.auto import *
import requests
from zipfile import ZipFile


def download_dataset_from_urls(urls, dataset_name, download_dir, extract_dir,
                               unzip=True, chunkSize=8192):
    # Create paths
    dataset_download_path = os.path.join(download_dir, dataset_name)
    dataset_extract_path = os.path.join(extract_dir, dataset_name)
    if os.path.isdir(dataset_download_path):
        shutil.rmtree(dataset_download_path)
    if os.path.isdir(dataset_extract_path):
        shutil.rmtree(dataset_extract_path)
    os.makedirs(dataset_download_path)
    os.makedirs(dataset_extract_path)
    # Download each url as a zip file.
    print("Downloading zip files to folder: {}".format(dataset_download_path))
    if unzip:
        print("Extracting zip files to folder: {}".format(dataset_extract_path))
    for i, url in enumerate(urls):
        # Create a temp. dir for this specific url
        name = "{}_url_{}".format(dataset_name, i)
        url_temp_path = "{}.zip".format(
            os.path.join(dataset_download_path, name))
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            pbar = tqdm(
                total=int(r.headers['Content-Length']), desc="{}".format(name))
            with open(url_temp_path, "wb+") as f:
                for chunk in r.iter_content(chunk_size=chunkSize):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        pbar.update(len(chunk))
        if unzip:
            with ZipFile(url_temp_path, 'r') as zipObj:
                # Extract all the contents of zip file in different directory
                extract_path = os.path.join(dataset_extract_path, name)
                os.makedirs(extract_path)
                zipObj.extractall(extract_path)


def read_urls_from_file(urls_file_path):
    assert os.path.isfile(urls_file_path)
    with open(urls_file_path, 'r') as f:
        lines = f.readlines()
        lines = lines[0].split("https")
        urls = ["https" + line.strip() for line in lines if len(line) > 0]
        return urls


def download_corpus_from_urls(corpus_name, urls_file_path, out_dir_path):
    # Create temp dirs.
    root_dir = os.path.join(out_dir_path, corpus_name)
    if os.path.isdir(root_dir):
        shutil.rmtree(root_dir)
    temp_dir = os.path.join(root_dir, "temp")
    extract_dir = os.path.join(temp_dir, "extract")
    download_dir = os.path.join(temp_dir, "download")
    os.makedirs(root_dir, exist_ok=True)
    os.makedirs(extract_dir)
    os.makedirs(download_dir)
    # Read the urls
    urls = read_urls_from_file(urls_file_path)[:1]
    print("Read {} urls from file {}".format(len(urls), urls_file_path))
    download_dataset_from_urls(
        urls=urls,
        dataset_name=corpus_name,
        download_dir=download_dir,
        extract_dir=extract_dir,
        unzip=True,
        chunkSize=8192)
    # Move everything from download dir to output dir
    shutil.move(os.path.join(download_dir, corpus_name), root_dir)
    # Remove temps
    shutil.rmtree(temp_dir)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--url_file', dest="url_file", type=str, required=True,
                        help="Path to file containing download urls")
    parser.add_argument("--out_dir", dest="out_dir", type=str, required=True,
                        help="Path to the output directory")
    args = parser.parse_args()
    download_corpus_from_urls("candor", args.url_file, args.out_dir)
