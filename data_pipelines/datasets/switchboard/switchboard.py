# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-20 13:05:13
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-06-07 11:27:48

"""
This script contains custom dataset implementation for the Switchboard corpus 
using the datasets.BuilderConfig and datasets.GeneratorBasedBuilder objects. 
Link: https://huggingface.co/docs/datasets/package_reference/builder_classes

"""

import sys
import os
import glob
from dataclasses import dataclass

import datasets
from datasets import Value, Audio, Array3D

from data_pipelines.datasets.switchboard.readers import (
    ISIPAlignedCorpusReader,
    LDCAudioCorpusReader,
)

from typing import Dict


_LDC_HOMEPAGE = "https://catalog.ldc.upenn.edu/LDC97S62"
_LDC_DESCRIPTION = """\
    The Switchboard-1 Telephone Speech Corpus (LDC97S62) consists of\
    approximately 260 hours of speech and was originally\
    collected by Texas Instruments in 1990-1, under DARPA\
    sponsorship
    """
_LDC_CITATION = """\
    J. J. Godfrey, E. C. Holliman and J. McDaniel, "SWITCHBOARD: telephone\
    speech corpus for research and development," [Proceedings] ICASSP-92: 1992\
    IEEE International Conference on Acoustics, Speech, and Signal Processing,\
     1992, pp. 517-520 vol.1, doi: 10.1109/ICASSP.1992.225858."""


_LDC_AUDIO_CORPUS_URL = "https://catalog.ldc.upenn.edu/LDC97S62"


class SwitchboardConfig(datasets.BuilderConfig):
    """
    Base class for DatasetBuilder data configuration.

    DatasetBuilder subclasses with data configuration options should subclass
    BuilderConfig and add their own properties.

    Link: https://huggingface.co/docs/datasets/v2.12.0/en/package_reference/builder_classes#datasets.BuilderConfig
    """

    def __init__(
        self,
        homepage: str,
        description: str,
        citation: str,
        data_url: str,
        features: Dict,
        **kwargs,
    ):
        """
        Configuration for the Switchboard corpus, which are used to build the
        dataset.
        Accepts additional kwargs that may be accepted by any dataset
        https://huggingface.co/docs/datasets/package_reference/loading_methods


        Parameters
        ----------
        homepage : str
            Link to the homepage for the corpus variant.
        description : str
            Corpus variant specific description.
        citation : str
            Citation for the corpus variant
        data_url : str
            URL for the corpus variant where it can be downloaded from. Empty
            string if there is no download link.
        features : Dict
            Dictionary representing the features that a specific corpus variant
            provides.
        """
        super().__init__(**kwargs)
        self.homepage = homepage
        self.description = description
        self.citation = citation
        self.data_url = data_url
        self.features = features


class Switchboard(datasets.GeneratorBasedBuilder):
    """
    Base class for datasets with data generation based on dict generators.

    GeneratorBasedBuilder is a convenience class that abstracts away much of
    the data writing and reading of DatasetBuilder. It expects subclasses to
    implement generators of feature dictionaries across the dataset splits
    (_split_generators). See the method docstrings for details.

    Link: https://huggingface.co/docs/datasets/v2.12.0/en/package_reference/builder_classes#datasets.DatasetBuilder
    """

    BUILDER_CONFIGS = [
        SwitchboardConfig(
            name="isip-aligned",
            homepage="https://isip.piconepress.com/projects/switchboard/",
            description="""`\
                Several lexicon items were fixed in the 10/19/02 release, and\
                about 45 start/stop times that had negative durations\
                (stop time preceded the start time) were repaired. We are no\
                longer actively developing this resource, but continue to\
                include bug fixes. Included in this release are the final\
                transcriptions for the entire database, the complete lexicon,\
                and automatic word alignments.
                """
            + "\n"
            + _LDC_DESCRIPTION,
            citation=_LDC_CITATION,
            data_url="https://www.isip.piconepress.com/projects/switchboard/releases/switchboard_word_alignments.tar.gz",
            features={
                "session": Value("string"),
                "participant": Value("string"),
                "turns": [
                    {
                        "start": Value("float"),
                        "end": Value("float"),
                        "text": Value("string"),
                        "tokens": [
                            {
                                "start": Value("float"),
                                "end": Value("float"),
                                "text": Value("string"),
                            }
                        ],
                    }
                ],
            },
        ),
        # NOTE: The ldc-audio requires the unzipped data directory path for now.
        SwitchboardConfig(
            name="ldc-audio",
            homepage=_LDC_HOMEPAGE,
            description=_LDC_DESCRIPTION,
            citation=_LDC_CITATION,
            data_url="",
            features={
                "session": Value("string"),
                "participant": Value("string"),
                "audio_paths": {
                    "stereo": Value("string"),
                    "mono": Value("string"),
                },
            },
        ),
    ]

    ############################ Overridden Methods ##########################

    @property
    def manual_download_instructions(self):
        if self.config.name == "ldc-audio":
            return (
                f"To use some variants of the Switchboard, you have to download "
                f"it manually. The audio is available at {_LDC_AUDIO_CORPUS_URL}."
            )

    def _info(self):
        return datasets.DatasetInfo(
            description=self.config.description,
            citation=self.config.citation,
            homepage=self.config.homepage,
            features=datasets.Features(self.config.features),
        )

    def _split_generators(self, dl_manager: datasets.DownloadManager):
        # Initialize the specific type of corpus.
        # Select the reader
        if self.config.name == "isip-aligned":
            extracted_path = dl_manager.download_and_extract(
                self.config.data_url
            )
            self.reader = ISIPAlignedCorpusReader(extracted_path)
        elif self.config.name == "ldc-audio":
            extracted_path = self.config.data_dir
            if not os.path.isdir(extracted_path):
                raise FileNotFoundError(
                    f"{extracted_path} does not exist. Make sure you insert "
                    f"a manual dir via `datasets.load_dataset('matinf', data_dir=...)` "
                    f"Manual download instructions: {self.manual_download_instructions}"
                )
            self.reader = LDCAudioCorpusReader(extracted_path)
        else:
            raise NotImplementedError()
        sessions = self.reader.get_sessions()
        return [
            datasets.SplitGenerator(
                name="full", gen_kwargs={"sessions": sessions}
            )
        ]

    def _generate_examples(self, sessions):
        for session in sessions:
            for participant in self.reader.PARTICIPANTS:
                if self.config.name == "isip-aligned":
                    conv = self.reader.get_session_transcript(
                        session, participant
                    )
                    yield f"{session}_{participant}", {
                        "session": session,
                        "participant": participant,
                        "turns": conv,
                    }
                elif self.config.name == "ldc-audio":
                    mono_path = self.reader.mono_paths[session][participant]
                    yield f"{session}_{participant}", {
                        "session": session,
                        "participant": participant,
                        "audio_paths": {
                            "stereo": self.reader.wav_paths[session],
                            "mono": mono_path,
                        },
                    }
                else:
                    raise NotImplementedError()
