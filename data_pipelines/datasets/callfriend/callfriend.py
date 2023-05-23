# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-19 14:30:32
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-05-23 11:19:44

import os

import datasets
from datasets import Value

from data_pipelines.datasets.callfriend.download import CallFriendDownloader

from data_pipelines.datasets.callfriend.utils import (
    get_utterances,
    get_audio_path,
    get_conversations,
)

_CALLFRIEND_HOMEPAGE = "https://catalog.ldc.upenn.edu/LDC96S46"
_CALLFRIEND_DESCRIPTION = """\
    The corpus consists of 60 unscripted telephone conversations,
    lasting between 5-30 minutes. The corpus also includes documentation
    describing speaker information (sex, age, education, callee telephone number)
    and call information (channel quality, number of speakers)."""
_CALLFRIEND_CITATION = """\
    @article{canavan1996callfriend,
    title={Callfriend american english-non-southern dialect},
    author={Canavan, Alexandra and Zipperlen, George},
    journal={Linguistic Data Consortium, Philadelphia},
    volume={10},
    number={1},
    year={1996}
}"""

_DEFAULT_FEATURES = {
    "id": Value("string"),
    "utterances": [
        {
            "speaker": Value("string"),
            "start": Value("float"),
            "end": Value("float"),
            "text": Value("string"),
        }
    ],
}

_AUDIO_FEATURES = {
    "id": Value("string"),
    "path": Value("string"),
}


class CallHomeConfig(datasets.BuilderConfig):
    def __init__(self, language, **kwargs):
        super().__init__(**kwargs)
        self.language = language


class CallHome(datasets.GeneratorBasedBuilder):
    _CACHE_DIR = "callfriend"

    BUILDER_CONFIGS = [
        CallHomeConfig(
            name="default",
            language="eng-n",
        ),
        CallHomeConfig(
            name="audio",
            language="eng-n",
        ),
    ]

    ############################ Overridden Methods ##########################

    def _info(self):
        return datasets.DatasetInfo(
            description=_CALLFRIEND_DESCRIPTION,
            citation=_CALLFRIEND_CITATION,
            homepage=_CALLFRIEND_HOMEPAGE,
            features=datasets.Features(
                _DEFAULT_FEATURES
                if self.config.name == "default"
                else _AUDIO_FEATURES
            ),
        )

    def _split_generators(self, dl_manager: datasets.DownloadManager):
        # Download the corpus
        dataset_dir = os.path.join(
            dl_manager.download_config.cache_dir, self._CACHE_DIR
        )
        downloader = CallFriendDownloader(
            output_dir=dataset_dir,
            language=self.config.language,
            force_download=dl_manager.download_config.force_download,
        )
        self.download_paths = downloader()
        # Obtain the conversations
        conversations = get_conversations(
            self.download_paths.transcriptions_dir
        )
        return [
            datasets.SplitGenerator(
                name="full", gen_kwargs={"conversations": conversations}
            )
        ]

    def _generate_examples(self, conversations):
        for conversation in conversations:
            if self.config.name == "default":
                # Get the utterances
                utterances = get_utterances(
                    self.download_paths.transcriptions_dir, conversation
                )
                yield f"{conversation}", {
                    "id": conversation,
                    "utterances": utterances,
                }
            elif self.config.name == "audio":
                path = get_audio_path(
                    self.download_paths.media_dir, conversation
                )
                if not os.path.isfile(path):
                    continue
                yield f"{conversation}", {
                    "id": conversation,
                    "path": path,
                }
