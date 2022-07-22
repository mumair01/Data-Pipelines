# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-22 11:56:49
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-22 13:59:20
import sys
import os
import glob

import datasets
from datasets import Value, Audio, Array3D

from data_pipelines.datasets.utils import (
    get_train_val_test_splits, extract_feature_set,read_txt
)

from data_pipelines.datasets.fisher.readers import LDCTranscriptsReader


_FISHER_HOMEPAGE = ""
_FISHER_DESCRIPTION = """"""
_FISHER_CITATION = ""

_DEFAULT_FEATURES = {
    "session" : Value('string'),
    "utterances" : [{
        "start" : Value("string"),
        "end" : Value('string'),
        "speaker" : Value('string'),
        "text" : Value('string')
    }]
}

_TEST_SPLIT_SIZE = 0.25
_VAL_SPLIT_SIZE = 0.2
_GLOBAL_SEED = 42

class FisherConfig(datasets.BuilderConfig):

    def __init__(self, homepage, description, features, test_size, val_size, seed, **kwargs):
        super().__init__(**kwargs)
        self.homepage = homepage
        self.description = description
        self.features = features
        self.test_size = test_size
        self.val_size = val_size
        self.seed = seed

class Fisher(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        FisherConfig(
            name="default",
            homepage = "",
            description = "",
            features=_DEFAULT_FEATURES,
            test_size=_TEST_SPLIT_SIZE,
            val_size=_VAL_SPLIT_SIZE,
            seed=_GLOBAL_SEED
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=self.config.description,
            citation=_FISHER_CITATION ,
            homepage=self.config.homepage,
            features=datasets.Features(self.config.features)
        )

    def _split_generators(self, dl_manager : datasets.DownloadManager):
        # NOTE: The data must be manually downloaded and specified in
        # self.config.data_dir
        if self.config.name == "default":
            self.reader = LDCTranscriptsReader(self.config.data_dir)
        else:
            raise NotImplementedError()
        # Generate the data splits
        tmp_path = os.path.join(self.config.data_dir,"splits")
        os.makedirs(tmp_path,exist_ok=True)
        sessions = self.reader.get_sessions()
        train, val, test = get_train_val_test_splits(
            sessions,self.config.test_size, self.config.val_size,self.
            config.seed)
        splits = {}
        for split, dialogues in zip(
                ('train','validation','test'), (train, val,test)):
            path = os.path.join(tmp_path,"{}.txt".format(split))
            with open(path, 'w') as f:
                f.writelines("\n".join(dialogues))
                splits[split] = path
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath" : splits['train']}),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath" : splits['validation']}),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath" : splits['test']}),
        ]

    def _generate_examples(self, filepath):
        sessions = read_txt(filepath)
        for session in sessions:
            if self.config.name == "default":
                conv = self.reader.get_session_transcript(session)
                yield f"{session}", {
                    "session" : session,
                    "utterances" : conv
                }
