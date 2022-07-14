# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-14 16:45:52
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-14 16:59:59

import sys
import os
import shutil
from glob import glob

from src.datasets.utils import (
    download_from_url, download_zip_from_url,
    extract_from_zip)

class CandorDownloader:

    DOWNLOAD_DIR = "."
    TEMP_DIR = os.path.join(DOWNLOAD_DIR,"temp")

    def __init__(self, urls_file_path : str, output_dir : str ):
        self.urls_file_path = urls_file_path
        # Create the dirs
        self.download_dir = os.path.join(output_dir,self.DOWNLOAD_DIR)
        self.temp_dir = os.path.join(output_dir,self.TEMP_DIR)
        self.output_dir = output_dir

    def __call__(self):
        if os.path.isdir(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        os.makedirs(self.temp_dir)
        # Download from each url individually
        urls = self.__read_candor_urls_from_file(self.urls_file_path)
        for i, url in enumerate(urls):
            download_zip_from_url(url,self.temp_dir)
        shutil.move(self.temp_dir,self.output_dir)
        return self.output_dir

    def __read_candor_urls_from_file(urls_file_path):
        assert os.path.isfile(urls_file_path)
        with open(urls_file_path, 'r') as f:
            lines = f.readlines()
            lines = lines[0].split("https")
            urls = ["https" + line.strip() for line in lines if len(line) > 0]
            return urls