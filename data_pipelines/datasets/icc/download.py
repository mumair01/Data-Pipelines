# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2023-08-22 10:35:30
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-08-22 10:36:13

################
# Contains the download class that is able to download a curated ICC corpus
# from the TTS cloud storage set up for the Human Interaction Lab.
################

from dataclasses import dataclass
import shutil
import os
import json
from typing import Type

class GenericDownloader:
    """
    Utility for downloading both the annotations and dialogues from useful corpera
    """

    def __init__(self, metadata_path: str, output_dir: str, force_download: bool = False) -> None:
        self.output_dir = output_dir
        self.metadata_path = metadata_path
        self.force_download = force_download

        with open(metadata_path) as f: 
            self.metadata = json.load(f)
        
        for key, value in self.metadata.items():
            setattr(self, key, value)

        if not self.__verify:
            raise FileNotFoundError(
                f"ERROR: {self.metadata_path} is not found."
            )
        
        if force_download and os.path.isdir(self.output_dir):
            shutil.rmtree(self.output_dir)

    def __call__(self):
        DownloadPaths = self.__generate_dataclass()
        paths = self.__download_files()
        return DownloadPaths(
            **paths
        )

    def __download_files(self, download_func, **kwargs):
        return download_func(**kwargs)

    def __generate_dataclass(self) -> Type:
        fields = [(key, str) for key in self.metadata.keys()]
        return dataclass("DownloadPaths", fields)                
    
    def __verify(self) -> bool:
        return (
            os.path.exists(self.metadata_path)
        )
    