# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-19 14:30:32
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-06-07 11:10:22

"""
This script contains custom dataset implementation for the Callfriend corpus 
using the datasets.BuilderConfig and datasets.GeneratorBasedBuilder objects. 
Link: https://huggingface.co/docs/datasets/package_reference/builder_classes

"""

import sys
import os
import glob

import datasets
from datasets import Value, Audio, Array3D

from data_pipelines.datasets.callhome.download import CallHomeDownloader

from data_pipelines.datasets.callhome.utils import (
    get_utterances,
    get_audio_path,
)

_CALLHOME_HOMEPAGE = "https://catalog.ldc.upenn.edu/LDC97S42"
_CALLHOME_DESCRIPTION = """\
    CALLHOME American English Speech was developed by the Linguistic Data
    Consortium (LDC) and consists of 120 unscripted 30-minute telephone
    conversations between native speakers of English."""
_CALLHOME_CITATION = """\
    @inproceedings{post2013improved,
    title={Improved speech-to-text translation with the Fisher and Callhome Spanish-English speech translation corpus},
    author={Post, Matt and Kumar, Gaurav and Lopez, Adam and Karakos, Damianos and Callison-Burch, Chris and Khudanpur, Sanjeev},
    booktitle={Proceedings of the 10th International Workshop on Spoken Language Translation: Papers},
    year={2013}}
"""

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
    """
    Base class for DatasetBuilder data configuration.

    DatasetBuilder subclasses with data configuration options should subclass
    BuilderConfig and add their own properties.

    Link: https://huggingface.co/docs/datasets/v2.12.0/en/package_reference/builder_classes#datasets.BuilderConfig
    """

    def __init__(self, language, **kwargs):
        """
        Configuration for the Callhome corpus, which are used to build the
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


class CallHome(datasets.GeneratorBasedBuilder):
    """
    Base class for datasets with data generation based on dict generators.

    GeneratorBasedBuilder is a convenience class that abstracts away much of
    the data writing and reading of DatasetBuilder. It expects subclasses to
    implement generators of feature dictionaries across the dataset splits
    (_split_generators). See the method docstrings for details.

    Link: https://huggingface.co/docs/datasets/v2.12.0/en/package_reference/builder_classes#datasets.DatasetBuilder
    """

    _CACHE_DIR = "callhome"

    BUILDER_CONFIGS = [
        CallHomeConfig(
            name="default",
            language="eng",
        ),
        CallHomeConfig(
            name="audio",
            language="eng",
        ),
    ]

    ############################ Overridden Methods ##########################

    def _info(self):
        return datasets.DatasetInfo(
            description=_CALLHOME_DESCRIPTION,
            citation=_CALLHOME_CITATION,
            homepage=_CALLHOME_HOMEPAGE,
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
        downloader = CallHomeDownloader(
            output_dir=dataset_dir,
            language=self.config.language,
            force_download=dl_manager.download_config.force_download,
        )
        self.download_paths = downloader()
        # Generate the data splits
        tmp_path = os.path.join(dataset_dir, "splits")
        os.makedirs(tmp_path, exist_ok=True)
        conversations = glob.glob(
            "{}/*.cha".format(self.download_paths.transcriptions_dir)
        )
        # Obtain the conversations
        conversations = [
            os.path.splitext(os.path.basename(conv))[0]
            for conv in conversations
        ]
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
