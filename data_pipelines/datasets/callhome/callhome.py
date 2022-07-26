# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-19 14:30:32
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-26 14:13:55

import sys
import os
import glob

import datasets
from datasets import Value, Audio, Array3D

from data_pipelines.datasets.callhome.download import (
    CallHomeDownloader, DownloadPaths
)

from data_pipelines.datasets.callhome.utils import (
    get_utterances, get_audio_path
)

_CALLHOME_HOMEPAGE = ""
_CALLHOME_DESCRIPTION = ""
_CALLHOME_CITATION = ""

_DEFAULT_FEATURES = {
    "id" : Value('string'),
    "utterances" : [{
            "speaker" : Value("string"),
            "start" : Value("float"),
            "end" : Value("float"),
            "text" : Value("string"),
        }
    ],
}

_AUDIO_FEATURES = {
    "id" : Value('string'),
    "path" : Value("string"),
}

# _TEST_SPLIT_SIZE = 0.25
# _VAL_SPLIT_SIZE = 0.2
# _GLOBAL_SEED = 42


class CallHomeConfig(datasets.BuilderConfig):
    def __init__(self,language, **kwargs):
        super().__init__(**kwargs)
        self.language = language

class CallHome(datasets.GeneratorBasedBuilder):

    _CACHE_DIR = "callhome"

    BUILDER_CONFIGS = [
        CallHomeConfig(
            name="default",
            language='eng',
        ),
         CallHomeConfig(
            name="audio",
            language='eng',
        )
    ]

    ############################ Overridden Methods ##########################

    def _info(self):
        return datasets.DatasetInfo(
            description=_CALLHOME_DESCRIPTION,
            citation=_CALLHOME_CITATION ,
            homepage=_CALLHOME_HOMEPAGE,
            features=datasets.Features(_DEFAULT_FEATURES \
                if self.config.name == 'default' else _AUDIO_FEATURES)
        )

    def _split_generators(self, dl_manager : datasets.DownloadManager):
        # Download the corpus
        dataset_dir = os.path.join(
            dl_manager.download_config.cache_dir,self._CACHE_DIR)
        downloader = CallHomeDownloader(
            output_dir=dataset_dir,
            language=self.config.language,
            force_download=dl_manager.download_config.force_download)
        self.download_paths = downloader()
        # Generate the data splits
        tmp_path = os.path.join(dataset_dir,"splits")
        os.makedirs(tmp_path,exist_ok=True)
        conversations = glob.glob("{}/*.cha".format(
            self.download_paths.transcriptions_dir))
        # Obtain the conversations
        conversations = [os.path.splitext(os.path.basename(conv))[0] \
            for conv in conversations]
        return [
            datasets.SplitGenerator(
                name=datasets.Split.ALL,
                gen_kwargs={"conversations" : conversations}
            )
        ]

        # NOTE: Remove the following code block since splits are not inherently
        # generated in the data.
        # ------------------
        # train, val, test = get_train_val_test_splits(
        #     conversations,self.config.test_size, self.config.val_size,self.
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

    def _generate_examples(self, conversations):
        for conversation in conversations:
            if self.config.name == "default":
                # Get the utterances
                utterances = get_utterances(
                    self.download_paths.transcriptions_dir,conversation)
                yield f"{conversation}",{
                    "id" : conversation,
                    "utterances" : utterances
                }
            elif self.config.name == "audio":
                path = get_audio_path(
                    self.download_paths.media_dir,conversation)
                if not os.path.isfile(path):
                    continue
                yield f"{conversation}",{
                    "id" : conversation,
                    "path" : path,
                }





