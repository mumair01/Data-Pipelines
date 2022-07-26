# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-22 11:56:49
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-26 14:13:29
import sys
import os
import glob

import datasets
from datasets import Value

from data_pipelines.datasets.utils import (
    get_train_val_test_splits,read_txt
)

from data_pipelines.datasets.fisher.readers import (
    LDCTranscriptsReader, LDCAudioReader
)

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
_AUDIO_FEATURES = {
    "session" : Value('string'),
    "audio_paths" : {
        "stereo" : Value('string'),
        "A" : Value('string'),
        "B" : Value('string')
    }
}

# _TEST_SPLIT_SIZE = 0.25
# _VAL_SPLIT_SIZE = 0.2
# _GLOBAL_SEED = 42

class FisherConfig(datasets.BuilderConfig):

    def __init__(self, homepage, description, features, **kwargs):
        super().__init__(**kwargs)
        self.homepage = homepage
        self.description = description
        self.features = features

class Fisher(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        FisherConfig(
            name="default",
            homepage = "",
            description = "",
            features=_DEFAULT_FEATURES,
        ),
        FisherConfig(
            name="audio",
            homepage = "",
            description = "",
            features=_AUDIO_FEATURES,
        ),
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
        elif self.config.name == "audio":
            self.reader = LDCAudioReader(self.config.data_dir)
        sessions = self.reader.get_sessions()
        return [
            datasets.SplitGenerator(
                name=datasets.Split.ALL,
                gen_kwargs={"filepath" : sessions}),
        ]

        # NOTE: Remove the following code block since splits are not inherently
        # generated in the data.
        # ------------------
        # Generate the data splits
        # tmp_path = os.path.join(self.config.data_dir,"splits")
        # os.makedirs(tmp_path,exist_ok=True)
        # sessions = self.reader.get_sessions()
        # train, val, test = get_train_val_test_splits(
        #     sessions,self.config.test_size, self.config.val_size,self.
        #     config.seed)
        # splits = {}
        # for split, dialogues in zip(
        #         ('train','validation','test'), (train, val,test)):
        #     path = os.path.join(tmp_path,"{}.txt".format(split))
        #     with open(path, 'w') as f:
        #         f.writelines("\n".join(dialogues))
        #         splits[split] = path
        # return [
        #     datasets.SplitGenerator(
        #         name=datasets.Split.TRAIN,
        #         gen_kwargs={"filepath" : splits['train']}),
        #     datasets.SplitGenerator(
        #         name=datasets.Split.VALIDATION,
        #         gen_kwargs={"filepath" : splits['validation']}),
        #     datasets.SplitGenerator(
        #         name=datasets.Split.TEST,
        #         gen_kwargs={"filepath" : splits['test']}),
        # ]
         # ------------------

    def _generate_examples(self, sessions):
        for session in sessions:
            if self.config.name == "default":
                conv = self.reader.get_session_transcript(session)
                yield f"{session}", {
                    "session" : session,
                    "utterances" : conv
                }
            elif self.config.name == "audio":
                audio_paths = self.reader.get_session_transcript(session)
                yield f"{session}", {
                    "session" : session,
                    "audio_paths" : audio_paths
                }
