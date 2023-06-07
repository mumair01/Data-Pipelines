# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-19 14:30:32
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-06-07 11:07:42


"""
This script contains custom dataset implementation for the Callfriend corpus 
using the datasets.BuilderConfig and datasets.GeneratorBasedBuilder objects. 
Link: https://huggingface.co/docs/datasets/package_reference/builder_classes

"""

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


class CallFriendConfig(datasets.BuilderConfig):
    """
    Base class for DatasetBuilder data configuration.

    DatasetBuilder subclasses with data configuration options should subclass
    BuilderConfig and add their own properties.

    Link: https://huggingface.co/docs/datasets/v2.12.0/en/package_reference/builder_classes#datasets.BuilderConfig
    """

    def __init__(self, language: str, **kwargs):
        """
        Configuration for the Callfriend corpus, which are used to build the
        dataset.
        Accepts additional kwargs that may be accepted by any dataset
        https://huggingface.co/docs/datasets/package_reference/loading_methods

        Parameters
        ----------
        language : str
            Language for the callfriend corpus
        """
        super().__init__(**kwargs)
        self.language = language


class CallFriend(datasets.GeneratorBasedBuilder):
    """
    Base class for datasets with data generation based on dict generators.

    GeneratorBasedBuilder is a convenience class that abstracts away much of
    the data writing and reading of DatasetBuilder. It expects subclasses to
    implement generators of feature dictionaries across the dataset splits
    (_split_generators). See the method docstrings for details.

    Link: https://huggingface.co/docs/datasets/v2.12.0/en/package_reference/builder_classes#datasets.DatasetBuilder
    """

    _CACHE_DIR = "callfriend"

    BUILDER_CONFIGS = [
        CallFriendConfig(
            name="default",
            language="eng-n",
        ),
        CallFriendConfig(
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
