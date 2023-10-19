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
from collections.abc import Callable

class GenericDownloader:
    """
    Utility for downloading both the annotations and dialogues from useful corpora
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

    def __download_files(self, download_func: Callable, *args, **kwargs):
        return download_func(*args, **kwargs)

    def __generate_dataclass(self) -> Type:
        fields = [(key, str) for key in self.metadata.keys()]
        return dataclass("DownloadPaths", fields)                
    
    def __verify(self) -> bool:
        return (
            os.path.exists(self.metadata_path)
        )

class TTSClusterDownloader(GenericDownloader):
    """
    Utility for downloading both the annotations and dialogues from useful corpora from the TTS Cluster
    """
    def __init__(self) -> None:
        super().__init__()
        # authentication methods

    def __call__(self, root_dir: str | os.PathLike, relative_paths: list[str | os.PathLike]):
        DownloadPaths = self.__generate_dataclass()
        paths_to_downloads = self.__get_paths_to_downloads(root_dir=root_dir, relative_paths=relative_paths)
        pathsets = self.__download_folders(paths_to_downloads=paths_to_downloads)
        return [DownloadPaths(**pathset) for pathset in pathsets]
            
    def __get_paths_to_downloads(self, root_dir: str | os.PathLike, relative_paths: list[str | os.PathLike]) -> list[str | os.PathLike]:
        return [os.path.join(root_dir, rel_path) for rel_path in relative_paths]

    def __download_func(self):
        paths = self.download_paths # from metadata.json, should be a list of highest-level paths
        for path in paths:
            shutil.copytree(path, self.output_dir)

    def __download_folders(self, paths_to_downloads: list[str | os.PathLike]) -> list[Type]:
        return [self.__download_files(self.__download_func, path_to_downloads) for path_to_downloads in paths_to_downloads]

    def upload_folder(self, folder_to_upload: str | os.PathLike, dest_paths: list[str | os.PathLike]):
        for path in dest_paths:
            shutil.copytree(folder_to_upload, path)

    def upload_file(self, file_to_upload: str | os.PathLike, dest_paths: list[str | os.PathLike]):
        for path in dest_paths:
            shutil.copy2(file_to_upload, path)