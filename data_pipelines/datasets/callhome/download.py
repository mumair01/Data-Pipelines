# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-19 14:39:35
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-19 16:30:15

import os
import sys
import urllib3
from bs4 import BeautifulSoup
from dataclasses import dataclass

from data_pipelines.datasets.utils import (
    download_from_url, download_zip_from_url, reset_dir
)

@dataclass
class DownloadPaths:
    transcriptions_dir : str
    media_dir : str

class CallHomeDownloader:

    BASE_TRANS_URL = "https://ca.talkbank.org/data/CallHome/{}.zip"
    BASE_MEDIA_URL = "https://media.talkbank.org/ca/CallHome"

    _LANGUAGES = [
        'ara','deu','eng','jpn','spa','zho'
    ]

    _DOWNLOAD_DIR = "."
    _BASE_TRANS_DOWNLOAD_DIR = os.path.join(_DOWNLOAD_DIR,"transcripts")
    _BASE_MEDIA_DOWNLOAD_DIR = os.path.join(_DOWNLOAD_DIR,"media")
    _TEMP_DIR = os.path.join(_DOWNLOAD_DIR,"temp")

    def __init__(self, output_dir : str, language="eng",
            force_download : bool = False):
        assert language in self._LANGUAGES,\
             f"language must be one of: {self._LANGUAGES}"

        self.language = language
        # Creating the directories.
        self.download_dir = os.path.join(output_dir,self._DOWNLOAD_DIR)
        self.trans_dir = os.path.join(
            self.download_dir,self._BASE_TRANS_DOWNLOAD_DIR)
        self.media_dir = os.path.join(
            self.download_dir,self._BASE_MEDIA_DOWNLOAD_DIR,language)
        # Creating the urls
        self.trans_url = self.BASE_TRANS_URL.format(language)
        self.media_url = os.path.join(self.BASE_MEDIA_URL,language)
        self.cached = os.path.isdir(self.trans_dir) and \
            os.path.isdir(self.media_dir) and \
            not force_download

    def __call__(self):
        if not self.cached:
            self.__download_transcripts()
            self.__download_media()
        return DownloadPaths(
            os.path.join(self.trans_dir,self.language),
            self.media_dir)

    def __download_transcripts(self):
        reset_dir(self.trans_dir)
        print(self.trans_url)
        download_zip_from_url(self.trans_url,self.trans_dir)

    def __download_media(self):
        # Scare the website for the audio filenames
        http = urllib3.PoolManager()
        resp = http.request('GET',self.media_url)
        soup = BeautifulSoup(resp.data,"html.parser")
        hrefs = soup.findAll('a',href=True)
        filenames = [h.text for h in hrefs if '.mp3' in h.text]
        # Download the files
        reset_dir(self.media_dir)
        for file in filenames:
            url = "{}/{}".format(self.media_url,file)
            download_from_url(url,"{}/{}".format(self.media_dir,file))
            break