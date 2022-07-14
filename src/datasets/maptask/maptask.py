# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-14 12:59:19
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-14 16:39:21

import sys
import os
import glob
import datasets
from datasets.utils.file_utils import (
    get_from_cache,
    hash_url_to_filename,
    url_or_path_join,
)


from src.datasets.maptask.download import MapTaskDownloader
from src.datasets.utils import download_from_url, download_zip_from_url,\
                                extract_from_zip, stereo_to_mono



class MapTaskConfig(datasets.BuilderConfig):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MapTask(datasets.GeneratorBasedBuilder):

    # Info vars.
    _HOMEPAGE = "https://groups.inf.ed.ac.uk/maptask/"
    _DESCRIPTION = "Maptask corpus custom dataset"
    _CITATION = "University of Edinburgh. HCRC Map Task Corpus LDC93S12. Web Download. Philadelphia: Linguistic Data Consortium, 1993."
    _FEATURES = {}

    # Other custom cars.
    # Custom vars.

    _ANNOTATIONS_URL = "http://groups.inf.ed.ac.uk/maptask/hcrcmaptask.nxtformatv2-1.zip"
    _STEREO_SIGNALS_URL = "https://groups.inf.ed.ac.uk/maptask/signals/dialogues/"

    # Superclass overridden vars.
    BUILDER_CONFIGS = [MapTaskConfig(name="default", description="maptask-v02")]


    ############################ Overridden Methods ##########################

    def _info(self):
        return datasets.DatasetInfo(
            description=self._DESCRIPTION,
            citation=self._CITATION,
            homepage=self._HOMEPAGE,
            features=datasets.Features(self._FEATURES)
        )

    def _split_generators(self, dl_manager : datasets.DownloadManager):
        """
        Downloads or retrieves the requested data files, organizes them into
        splits, and defines specific arguments for the generation process.
        """
        print("IN SPLIT GENERATORS!")
        # Download the dataset first.
        gfc = self.__get_from_cache(dl_manager)
        print()
        print("gfc",gfc)
        if gfc is None or dl_manager.download_config.force_download:
            downloader = MapTaskDownloader(dl_manager.download_config.cache_dir)
            annotations_path = downloader.download_annotations()
            stereo_output_path, mono_output_path = downloader.download_signals()
        # Generate the data splits


    def _generate_examples(self):
        pass

    ############################## HELPER METHODS ############################

    def __get_from_cache(self, dl_manager):
        try:
            cache_dir = dl_manager.download_config.cache_dir
            max_retries = dl_manager.download_config.max_retries
            for url in [self._ANNOTATIONS_URL, self._STEREO_SIGNALS_URL]:
                gfc = get_from_cache(
                    url,
                    cache_dir=cache_dir,
                    local_files_only=True,
                    use_etag=False,
                    max_retries=max_retries,
                )
            return gfc
        except FileNotFoundError:
            return None