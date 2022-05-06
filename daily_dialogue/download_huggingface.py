# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-03-09 14:09:09
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-06 16:02:49

# NOTE: Downloads the daily dialogue corpus from huggingface.

import shutil
import argparse
import itertools
from copy import deepcopy
from sklearn.utils import shuffle
import re
from datasets import load_dataset
import os
import numpy as np
import tensorflow as tf
import sklearn
assert sklearn.__version__ >= "0.20"
# TensorFlow ≥2.0 is required
assert tf.__version__ >= "2.0"
# Common imports


def preprocess_huggingface_daily_dialogue(dataset):
    # Copy to avoid changing original
    dataset = deepcopy(dataset)
    # Shuffle on conversation level
    dataset = shuffle(dataset)
    # For each utterance, split by punctuation
    for i in range(len(dataset)):
        conv = dataset[i]
        # NOTE: Assumption is that there are two speakers per conversation
        processed_conv = []
        for j in range(len(conv)):
            target_str = conv[j].strip()
            split_toks = re.split(r"\. |\? ", target_str)
            split_toks = [tok for tok in split_toks if len(tok) > 0]
            # Remove all punctuation and lowercase all
            split_toks = [re.sub(r'[^\w\s]', '', tok).lower()
                          for tok in split_toks]
            # Remove any double whitespaces
            split_toks = [re.sub(' +', ' ', tok).lower() for tok in split_toks]
            # Add the speaker tokens for each turn
            split_toks = ["[SP{}] ".format((j % 2) + 1) + tok +
                          "[SP{}]".format((j % 2) + 1) for tok in split_toks]
            processed_conv.extend(split_toks)
        dataset[i] = processed_conv
    # For each conversation, add start and end tokens
    dataset = [["[START]"] + conv + ["[END]"] for conv in dataset]
    # Flatten the data
    dataset = list(itertools.chain(*dataset))
    # return dataset
    return dataset


def save_processed_to_file(save_dir, filename, dataset):
    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, filename)+".txt", "w") as f:
        for item in dataset:
            f.writelines(item + "\n")


def parse_and_save_dd_dataset(datasets, dataset_type, output_dir):
    dataset = datasets[dataset_type]['dialog']
    processed_dataset = preprocess_huggingface_daily_dialogue(dataset)
    save_processed_to_file(
        output_dir, dataset_type, processed_dataset)


def download_daily_dialogue(output_dir, seed=None):
    """
    Download the daily dialogue dataset and store it in files that
    can be used for trainingand evaluation.
    """
    os.makedirs(output_dir, exist_ok=True)
    if seed != None:
        np.random.seed(seed)
    print("Downloading dataset...")
    datasets = load_dataset('daily_dialog')
    # Create the save directory
    result_dir = os.path.join(output_dir, "daily_dialog")
    if os.path.isdir(result_dir):
        shutil.rmtree(result_dir)
    os.makedirs(result_dir, exist_ok=True)
    # Parse and save training, val, and test splits.
    for dataset_type in ("train", "validation", "test"):
        print("Parsing and saving split: {}".format(dataset_type))
        parse_and_save_dd_dataset(datasets, dataset_type, result_dir)
    print("Daily dialog downloaded to: {}".format(output_dir))


if __name__ == "__main__":
    # Obtain args
    parser = argparse.ArgumentParser()
    parser.add_argument("--out_dir", dest="out_dir", type=str, required=True,
                        help="Path to the output directory")
    args = parser.parse_args()
    # Download the daily dialog dataset
    download_daily_dialogue(
        output_dir=args.out_dir,
        seed=42
    )
