# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-22 11:56:49
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-06-07 11:21:53

"""
This script contains custom dataset implementation for the Fisher corpus 
using the datasets.BuilderConfig and datasets.GeneratorBasedBuilder objects. 
Link: https://huggingface.co/docs/datasets/package_reference/builder_classes

"""


import sys
import os
import glob

import datasets
from datasets import Value
from typing import Dict

from data_pipelines.datasets.fisher.readers import (
    LDCTranscriptsReader,
    LDCAudioReader,
)

_FISHER_HOMEPAGE = "https://catalog.ldc.upenn.edu/LDC2004T19"
_FISHER_DESCRIPTION = """\
    Fisher English Training Speech Part 1 Transcripts was developed by the
    Linguistic Data Consortium (LDC) and contains time-aligned transcript data
    for 5,850 telephone conversations (984 hours) in English. In addition to
    the transcriptions, there is a complete set of tables describing the speakers,
    the properties of the telephone calls, and the set of topics that were used
    to initiate the conversations. The corresponding speech files for these
    transcripts are contained in Fisher English Training Speech Part 1 Speech
    (LDC2004S13).
"""
_FISHER_CITATION = """\
    @inproceedings{cieri2004fisher,
    title={The Fisher corpus: A resource for the next generations of speech-to-text.},
    author={Cieri, Christopher and Miller, David and Walker, Kevin},
    booktitle={LREC},
    volume={4},
    pages={69--71},
    year={2004}
    }
"""

_FISHER_LDC_SPEECH_URL = "https://catalog.ldc.upenn.edu/LDC2004T19"
_FISHER_LDC_TRANSCRIPTS_URL = "https://catalog.ldc.upenn.edu/LDC2004T19"


_DEFAULT_FEATURES = {
    "session": Value("string"),
    "utterances": [
        {
            "start": Value("string"),
            "end": Value("string"),
            "speaker": Value("string"),
            "text": Value("string"),
        }
    ],
}
_AUDIO_FEATURES = {
    "session": Value("string"),
    "audio_paths": {
        "stereo": Value("string"),
        "A": Value("string"),
        "B": Value("string"),
    },
}


class FisherConfig(datasets.BuilderConfig):
    """
    Base class for DatasetBuilder data configuration.

    DatasetBuilder subclasses with data configuration options should subclass
    BuilderConfig and add their own properties.

    Link: https://huggingface.co/docs/datasets/v2.12.0/en/package_reference/builder_classes#datasets.BuilderConfig
    """

    def __init__(
        self, homepage: str, description: str, features: Dict, **kwargs
    ):
        """
        Configuration for the Fisher corpus, which are used to build the
        dataset.
        Accepts additional kwargs that may be accepted by any dataset
        https://huggingface.co/docs/datasets/package_reference/loading_methods



        Parameters
        ----------
        homepage : str
            Link to the homepage for the corpus variant.
        description : str
            Corpus variant specific description.
        features : Dict
            Dictionary representing the features that a specific corpus variant
            provides.
        """
        super().__init__(**kwargs)
        self.homepage = homepage
        self.description = description
        self.features = features


class Fisher(datasets.GeneratorBasedBuilder):
    """
    Base class for datasets with data generation based on dict generators.

    GeneratorBasedBuilder is a convenience class that abstracts away much of
    the data writing and reading of DatasetBuilder. It expects subclasses to
    implement generators of feature dictionaries across the dataset splits
    (_split_generators). See the method docstrings for details.

    Link: https://huggingface.co/docs/datasets/v2.12.0/en/package_reference/builder_classes#datasets.DatasetBuilder
    """

    BUILDER_CONFIGS = [
        FisherConfig(
            name="default",
            homepage=_FISHER_HOMEPAGE,
            description=_FISHER_DESCRIPTION,
            features=_DEFAULT_FEATURES,
        ),
        FisherConfig(
            name="audio",
            homepage=_FISHER_HOMEPAGE,
            description=_FISHER_DESCRIPTION,
            features=_AUDIO_FEATURES,
        ),
    ]

    @property
    def manual_download_instructions(self):
        """
        String representation of the instructions required to download corpora
        that must be manually specified to construct into a dataaset.
        """
        return (
            f"To use Fisher you have to download it manually. The transcripts "
            f"can be downloaded from {_FISHER_LDC_TRANSCRIPTS_URL} and the audio "
            f"can be downloaded from {_FISHER_LDC_SPEECH_URL}"
        )

    def _info(self):
        return datasets.DatasetInfo(
            description=self.config.description,
            citation=_FISHER_CITATION,
            homepage=self.config.homepage,
            features=datasets.Features(self.config.features),
        )

    def _split_generators(self, dl_manager: datasets.DownloadManager):
        # NOTE: The data must be manually downloaded and specified in
        # self.config.data_dir

        if not os.path.isdir(self.config.data_dir):
            raise FileNotFoundError(
                f"{self.config.data_dir} does not exist. Make sure you insert "
                f"a manual dir via `datasets.load_dataset('matinf', data_dir=...)` "
                f"Manual download instructions: {self.manual_download_instructions}"
            )

        if self.config.name == "default":
            self.reader = LDCTranscriptsReader(self.config.data_dir)
        elif self.config.name == "audio":
            self.reader = LDCAudioReader(self.config.data_dir)
        sessions = self.reader.get_sessions()
        return [
            datasets.SplitGenerator(
                name="full", gen_kwargs={"sessions": sessions}
            ),
        ]

    def _generate_examples(self, sessions):
        for session in sessions:
            if self.config.name == "default":
                conv = self.reader.get_session_transcript(session)
                yield f"{session}", {"session": session, "utterances": conv}
            elif self.config.name == "audio":
                audio_paths = self.reader.get_session_transcript(session)
                yield f"{session}", {
                    "session": session,
                    "audio_paths": audio_paths,
                }
