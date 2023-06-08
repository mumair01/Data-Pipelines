# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-26 14:45:40
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-06-07 21:23:42

import os
import glob
import shutil
import datasets
import subprocess
from dataclasses import dataclass
from sys import platform

from typing import List, Dict, Callable

from data_pipelines.datasets.callfriend import (
    load_callfriend,
    VARIANTS as CF_VARIANTS,
    DETAILS as CF_DETAILS,
)
from data_pipelines.datasets.callhome import (
    load_callhome,
    VARIANTS as CH_VARIANTS,
    DETAILS as CH_DETAILS,
)
from data_pipelines.datasets.fisher import (
    load_fisher,
    VARIANTS as FISHER_VARIANTS,
    DETAILS as FISHER_DETAILS,
)
from data_pipelines.datasets.maptask import (
    load_maptask,
    VARIANTS as MT_VARIANTS,
    DETAILS as MT_DETAILS,
)
from data_pipelines.datasets.switchboard import (
    load_switchboard,
    VARIANTS as SB_VARIANTS,
    DETAILS as SB_DETAILS,
)

from data_pipelines.datasets.utils import reset_dir
from data_pipelines.paths import PkgPaths

_CACHE_DIR = PkgPaths.Core.cacheDir


@dataclass
class DsetConfig:
    """
    Container for configurations for a supported dataset
    """

    loader: Callable  # Method to load the dataset provided by each dataset
    variants: List[str]  # List of variants supported by the dataset
    details: Dict  # Dictionary containing greater details for that dataset.


class DataPipeline:
    """
    Provides methods to load various datasets
    """

    _DSETS = {
        "callfriend": DsetConfig(load_callfriend, CF_VARIANTS, CF_DETAILS),
        "callhome": DsetConfig(load_callhome, CH_VARIANTS, CH_DETAILS),
        "fisher": DsetConfig(load_fisher, FISHER_VARIANTS, FISHER_DETAILS),
        "maptask": DsetConfig(load_maptask, MT_VARIANTS, MT_DETAILS),
        "switchboard": DsetConfig(load_switchboard, SB_VARIANTS, SB_DETAILS),
    }

    def __init__(self, cache_dir: str = _CACHE_DIR):
        """_summary_

        Parameters
        ----------
        cache_dir : str, optional
            Path to the directory where generated dataset objects are stored,
            by default _CACHE_DIR
        downloads_dir : str, optional
            Path to the directory where raw datasets are downloaded,
            by default _DOWNLOADS_DIR
        """
        self._cache_dir = cache_dir
        self._downloads_dir = os.path.join(self.cache_dir, "downloads")

    @property
    def cache_dir(self) -> str:
        return self._cache_dir

    def clear_cache(self):
        """
        Remove all downloaded and saved datasets.
        NOTE: This will NOT remove the downloaded datasets. To do so, please
        specify the download_mode="force_redownload" in the load_dset method.
        """
        keep = [self._downloads_dir]
        paths = [
            os.path.join(self.cache_dir, p) for p in os.listdir(self.cache_dir)
        ]
        for path in paths:
            if not any([path.__contains__(k) for k in keep]):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                if os.path.isfile(path):
                    os.remove(path)

    def supported_dsets(self) -> List[str]:
        """
        Obtain a list of all supported datasets.

        Returns
        -------
        List[str]
        """
        return list(self._DSETS.keys())

    def load_dset(
        self,
        dataset: str,
        variant: str,
        download_mode: str = "reuse_dataset_if_exists",
        **kwargs,
    ) -> datasets.Dataset:
        """
        Load the specified dataset with dataset specific arguments provided as
        additional keyword arguments.

        NOTE: See link below for operation that can be performed on a dataset
        object that us returned.
        Link: https://huggingface.co/docs/datasets/v2.2.1/en/access

        Parameters
        ----------
        dataset : str
            Name of the supported dataset.
        variant : str
            Name of the variant to load
        download_mode : str:
            One of the following:
                1. reuse_dataset_if_exists --> Reuse everything.
                2. reuse_cache_if_exists --> Regenerate the dataset object from
                    existing cache.
                3. force_redownload --> Redownload everything.

        Returns
        -------
        datasets.Dataset:
            Dataset object that has all the methods provided by a huggingface
            dataset object.
            Link: https://huggingface.co/docs/datasets/v2.2.1/en/access
        """
        assert (
            dataset in self.supported_dsets()
        ), f"dataset must be one of: {self.supported_dsets()}"
        assert variant in self.dset_variants(
            dataset
        ), f"Unsupported variant {variant}, must be in {self.dset_variants(dataset)}"
        # Specify the cache directory
        kwargs.update({"cache_dir": _CACHE_DIR})
        return self._DSETS[dataset].loader(
            variant=variant, download_mode=download_mode, **kwargs
        )

    def dset_variants(self, dataset: str) -> List[str]:
        """
        Obtain the list of variants supported by the specified dataset.

        Parameters
        ----------
        dataset : str
            Name of the dataset.

        Returns
        -------
        List[str]
        """
        assert (
            dataset in self.supported_dsets()
        ), f"dataset must be one of: {self.supported_dsets()}"
        return list(self._DSETS[dataset].variants)

    def dset_details(self, dataset: str) -> Dict:
        """
        Obtain the details of the specified dataset.

        Parameters
        ----------
        dataset : str
            Name of the dataset.

        Returns
        -------
        Dict
        """
        assert (
            dataset in self.supported_dsets()
        ), f"dataset must be one of: {self.supported_dsets()}"
        return self._DSETS[dataset].details

    def open_downloads_dir(self, dataset: str):
        """
        Open the dataset in the system explorer for the specified dataset

        Parameters
        ----------
        dataset : str
            Name of the dataset for which the raw downloaded directory should be
            opened

        Raises
        ------
        Exception
            Raised if the dataset download directory is not found.
        NotImplementedError
            Raised if the underlying platform is not supported.
        """
        assert (
            dataset in self.supported_dsets()
        ), f"dataset must be one of: {self.supported_dsets()}"

        dset_download_path = os.path.join(self._downloads_dir, dataset)

        if not os.path.isdir(dset_download_path):
            raise Exception(
                f"No download directory found for dataset {dataset} at: {dset_download_path}"
            )

        if platform == "linux" or platform == "linux2":
            # linux
            raise NotImplementedError()
        elif platform == "darwin":
            subprocess.run(["/usr/bin/open", dset_download_path])
        elif platform == "win32":
            # Windows...
            raise NotImplementedError()
