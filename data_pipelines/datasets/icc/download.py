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
from getpass import getpass, getuser
import smbclient
from tqdm import tqdm

@dataclass
class DownloadPaths:
    """
    Stores the download paths of a generic file
    """
    download_path: str


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
    
    def __verify(self) -> bool:
        return (
            os.path.exists(self.metadata_path)
        )

class TTSClusterDownloader(GenericDownloader):
    """
    Utility for downloading both the annotations and dialogues from useful corpora from the TTS Cluster
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.username = getuser()
        self.password = getpass()
        self.domain_controller = input("Enter domain controller: ")
        self.path_to_share = input("Enter the path to the share: ")
        smbclient.ClientConfig(
            username=self.username,
            password=self.password,
            domain_controller=self.domain_controller
        )
    
    def __download_func(self):
        files = []
        paths = [fr"{self.path_to_share}\{d}" for d in smbclient.listdir(self.path_to_share) if d in self.download_paths]
        print('Retrieving files from Cold Storage...')
        for path in tqdm(paths):
            path_walk = [f for f in smbclient.walk(path)]
            for subdir_tup in path_walk[1:]:
                subdir = subdir_tup[0]
                subdir_files = subdir_tup[-1]
                files += [fr"{subdir}\{sdf}" for sdf in subdir_files]

        print('Writing files from Cold Storage...')
        for file in tqdm(files):
            with smbclient.open_file(file, 'rb') as f:
                this_file = f.read()
            dst_subdir = r'/'.join(file.split('\\')[6:-1])
            filename = file.split('\\')[-1]
            os.makedirs(fr"{self.output_dir}/{dst_subdir}", exist_ok=True)
            with open(fr'{self.output_dir}/{dst_subdir}/{filename}', 'wb') as f:
                f.write(this_file)
        return files
    
    def __download_files(self, download_func: Callable):
        return download_func()

    def __call__(self):
        paths = self.__download_files(self.__download_func)
        return [DownloadPaths(path) for path in paths]           

    def upload_to_share(self):
        paths_on_share = []
        for path in self.upload_paths: 
            with open(path, 'rb') as f:
                this_doc = f.read()
            
            upload_paths_split = path.split('/')
            if len(upload_paths_split) > 2:
                dst_subdir = '\\'.join(upload_paths_split[1:-1])
                full_dst = fr"{self.path_to_share}\{dst_subdir}"
                smbclient.makedirs(full_dst, exist_ok=True)
                dst_file_path = fr"{full_dst}\{upload_paths_split[-1]}"
                with smbclient.open_file(dst_file_path, 'wb') as f:
                    f.write(this_doc)
            else:
                dst_file_path = fr"{self.path_to_share}\{upload_paths_split[-1]}"
                with smbclient.open_file(dst_file_path, 'wb') as f:
                    f.write(this_doc)
            paths_on_share.append(dst_file_path)
        
        return [DownloadPaths(p) for p in paths_on_share]