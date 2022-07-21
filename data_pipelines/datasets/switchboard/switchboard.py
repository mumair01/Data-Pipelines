# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-20 13:05:13
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-21 15:38:46

import sys
import os
import glob
from dataclasses import dataclass

import datasets
from datasets import Value, Audio, Array3D

from data_pipelines.datasets.switchboard.isip import ISIPAlignedCorpusReader
from data_pipelines.datasets.switchboard.ldc import LDCAudioCorpusReader
from data_pipelines.datasets.utils import (
    get_train_val_test_splits, extract_feature_set
)

_LDC_HOMEPAGE = "https://catalog.ldc.upenn.edu/LDC97S62"
_LDC_DESCRIPTION = """\
    The Switchboard-1 Telephone Speech Corpus (LDC97S62) consists of
    approximately 260 hours of speech and was originally
    collected by Texas Instruments in 1990-1, under DARPA
    sponsorship
    """
_LDC_CITATION = """\
    J. J. Godfrey, E. C. Holliman and J. McDaniel, "SWITCHBOARD: telephone
    speech corpus for research and development," [Proceedings] ICASSP-92: 1992
    IEEE International Conference on Acoustics, Speech, and Signal Processing,
     1992, pp. 517-520 vol.1, doi: 10.1109/ICASSP.1992.225858."""

_DIALOG_FEATURES = {
    "start" : Value('float'),
    "end" : Value("float"),
    "word" : Value("string")
}

_TEST_SPLIT_SIZE = 0.25
_VAL_SPLIT_SIZE = 0.2
_GLOBAL_SEED = 42

class SwitchboardConfig(datasets.BuilderConfig):
    def __init__(self, homepage, description, citation, data_url, features,
            test_size, val_size, seed, **kwargs):
        super().__init__(**kwargs)
        self.homepage = homepage
        self.description = description
        self.citation = citation
        self.data_url = data_url
        self.features = features
        self.test_size = test_size
        self.val_size = val_size
        self.seed = seed

class Switchboard(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        SwitchboardConfig(
            name="isip-aligned",
            homepage = "https://isip.piconepress.com/projects/switchboard/",
            description = """`\
                Several lexicon items were fixed in the 10/19/02 release, and
                about 45 start/stop times that had negative durations
                (stop time preceded the start time) were repaired. We are no
                longer actively developing this resource, but continue to
                include bug fixes. Included in this release are the final
                transcriptions for the entire database, the complete lexicon,
                and automatic word alignments.
                """ + "\n" + _LDC_DESCRIPTION,
            citation=_LDC_CITATION,
            data_url="https://www.isip.piconepress.com/projects/switchboard/releases/switchboard_word_alignments.tar.gz",
            features={
                "session" : Value("string"),
                "participant" : Value("string"),
                "turns" : [{
                    "start" : Value('float'),
                    "end" : Value("float"),
                    "text" : Value("string"),
                    "tokens" : [{
                        "start" : Value('float'),
                        "end" : Value("float"),
                        "text" : Value("string"),
                    }]
                }]
            },
            test_size=_TEST_SPLIT_SIZE,
            val_size=_VAL_SPLIT_SIZE,
            seed=_GLOBAL_SEED
        ),
        # NOTE: The ldc-audio requires the unzipped data directory path for now.
        SwitchboardConfig(
            name="ldc-audio",
            homepage=_LDC_HOMEPAGE,
            description=_LDC_DESCRIPTION,
            citation=_LDC_CITATION,
            data_url="",
            features={
                "session" : Value('string'),
                "participant" : Value('string'),
                "audio_paths" : {
                    "stereo" : Value('string'),
                    "mono" : Value('string')
                },
                "egemaps" : {
                    "values" : Array3D(shape=(1,-1,25),dtype='float64'),
                    "features" : [Value("string")]
                },
            },
            test_size=_TEST_SPLIT_SIZE,
            val_size=_VAL_SPLIT_SIZE,
            seed=_GLOBAL_SEED
        )
    ]

    ############################ Overridden Methods ##########################

    def _info(self):
        return datasets.DatasetInfo(
            description=self.config.description,
            citation=self.config.citation,
            homepage=self.config.homepage,
            features=datasets.Features(self.config.features)
        )

    def _split_generators(self, dl_manager : datasets.DownloadManager):
        # Initialize the specific type of corpus.
        # Select the reader
        if self.config.name == "isip-aligned":
            extracted_path = dl_manager.download_and_extract(self.config.data_url)
            self.reader = ISIPAlignedCorpusReader(extracted_path)
        elif self.config.name == "ldc-audio":
            extracted_path = self.config.data_dir
            self.reader = LDCAudioCorpusReader(extracted_path)
        else:
            raise NotImplementedError()
        # Generate the data splits
        tmp_path = os.path.join(extracted_path,"splits")
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
        with open(filepath,'r') as f:
            sessions = [d.rstrip("\n") for d in f.readlines()]
            for session in sessions:
                for participant in self.reader.PARTICIPANTS:
                    if self.config.name == "isip-aligned":
                        conv = self.reader.get_session_transcript(
                            session,participant)
                        yield f"{session}_{participant}", {
                            "session" : session,
                            "participant" : participant,
                            "turns" : conv
                        }
                    elif self.config.name == "ldc-audio":
                        mono_path = self.reader.mono_paths[session][participant]
                        # Extract egemaps
                        egemaps = extract_feature_set(mono_path,'egemapsv02_50ms')
                        yield f"{session}_{participant}",{
                            "session" : session,
                            "participant" : participant,
                            "audio_paths" : {
                                "stereo" : self.reader.wav_paths[session],
                                "mono" : mono_path
                            },
                            "egemaps" : egemaps
                        }
                    else:
                        raise NotImplementedError()


