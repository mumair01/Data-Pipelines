# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-14 12:59:19
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-26 15:15:26

import sys
import os

import datasets
from datasets import Value, Audio, Array3D

from data_pipelines.datasets.maptask.download import MapTaskDownloader
from data_pipelines.datasets.maptask.utils import (
    get_dialogues,
    get_maptask_file,
    get_utterances,
    get_utterance_pos_annotations,
)
from data_pipelines.datasets.utils import (
    get_train_val_test_splits,
    # extract_feature_set
)
_MAPTASK_HOMEPAGE = "https://groups.inf.ed.ac.uk/maptask/"
_MAPTASK_DESCRIPTION = "Maptask corpus custom dataset"
_MAPTASK_CITATION = """\
    University of Edinburgh. HCRC Map Task Corpus LDC93S12. Web Download.
    Philadelphia: Linguistic Data Consortium, 1993.
    """
_DEFAULT_FEATURES = {
    "dialogue" : Value("string"),
    "participant" : Value("string"),
    "utterances" : [{
            "start" : Value("float"),
            "end" : Value("float"),
            "text" : Value("string"),
            "pos" : Value("string")
        }
    ],
}

_AUDIO_FEATURES = {
    "dialogue" : Value("string"),
    "participant" : Value("string"),
    "audio_paths" : {
        "stereo" : Value("string"),
        "mono" : Value("string"),
    },
}



class MapTaskConfig(datasets.BuilderConfig):
    """BuilderConfig for MapTask"""
    def __init__(self, **kwargs):
        """
        Args:
            test_size (float): Test split size b/w 0 and 1.
            val_size (float): Val split size b/w 0 and 1.
        """
        super().__init__(**kwargs)

class MapTask(datasets.GeneratorBasedBuilder):
    """
    Builder for the MapTask corpus.
    For details: https://huggingface.co/docs/datasets/v2.3.2/en/about_dataset_load
    """

    _MAPTASK_PARTICIPANTS  = ["f", "g"]
    _CACHE_DIR = "maptask"

    # Superclass overridden vars.
    BUILDER_CONFIGS = [
        MapTaskConfig(
            name="default",
            description=
                """\
                    Variant of the maptask corpus containing data parsed directly
                    from the corpus.
                """,
        ),
        MapTaskConfig(
            name="audio",
            description=
                """\
                    Variant of the maptask corpus containing various audio data.
                """,
        ),
    ]

    ############################ Overridden Methods ##########################

    def _info(self):
        return datasets.DatasetInfo(
            description=_MAPTASK_DESCRIPTION,
            citation=_MAPTASK_CITATION ,
            homepage=_MAPTASK_HOMEPAGE,
            features=datasets.Features(_DEFAULT_FEATURES \
                if self.config.name == "default" else _AUDIO_FEATURES),
        )

    def _split_generators(self, dl_manager : datasets.DownloadManager):
        """
        Downloads or retrieves the requested data files, organizes them into
        splits, and defines specific arguments for the generation process.
        """
        dataset_dir = os.path.join(
            dl_manager.download_config.cache_dir,self._CACHE_DIR)
        downloader = MapTaskDownloader(
            dataset_dir,
            force_download=dl_manager.download_config.force_download)
        self.download_paths = downloader()
        # Generate the data splits from the dialogues
        dialogues = get_dialogues(self.download_paths.annotations_path)
        return [
            datasets.SplitGenerator(
                name="full",
                gen_kwargs={"dialogues" : dialogues}),
        ]

    def _generate_examples(self, dialogues):
        for dialogue in dialogues:
            for participant in self._MAPTASK_PARTICIPANTS:
                if self.config.name == "default":
                # Get the utterances
                    utterances = get_utterances(self.download_paths.annotations_path,
                                    dialogue, participant)
                    # Get the parts of speech and add to the corresponding utterances
                    pos_annotations = get_utterance_pos_annotations(
                        self.download_paths.annotations_path,dialogue,participant)
                    for data in utterances:
                        data['pos'] = pos_annotations[data['end']] \
                            if data['end'] in pos_annotations else ''
                    yield f"{dialogue}.{participant}", {
                            "dialogue" : dialogue,
                            "participant" : participant,
                            "utterances" : utterances,
                        }
                elif self.config.name == "audio":
                    # Open the audio files
                    stereo_path = get_maptask_file(
                        self.download_paths.stereo_path,dialogue,"mix","wav")
                    mono_path = get_maptask_file(
                        self.download_paths.mono_path,dialogue,participant,"wav")
                    yield f"{dialogue}.{participant}", {
                        "dialogue" : dialogue,
                        "participant" : participant,
                        "audio_paths" : {
                            "stereo" : stereo_path,
                            "mono" : mono_path
                        }
                    }
