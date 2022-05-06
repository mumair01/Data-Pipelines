# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-03-03 09:54:27
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-03-17 10:16:06
"""
pipeline.py re-executes all data transformations described in the README

In order to produce a dataset, several steps are needed, but it is also
useful to repeat all steps from the beginning (say if changes are made
erroneously). Since some of the scripts alter files in place, the pipeline
cannot necessarily be re-run from the middle. So pipeline.py takes the
basic linguistic consortium and msu files and re-creates the csvs for the
project.
"""

import re_utterizer
import merge
import map_acts
# import sentence_classification
import cha_to_csv
import add_fto

BASE_DIR = "./"


def data_pipeline():
    """ For all files in the BASE_DIR, push them through
    the data pipeline from raw Linguistic Consortium and
    Mississippi State U files to usable .csv and .cha files"""

    print("\nRe-utterizing:")
    # src_dir = "lc-sb/"
    # dest_dir = "lc-sb2/"
    # re_utterizer.re_utterize(BASE_DIR, src_dir, dest_dir)

    print("\nMerging:")
    # lc_src = dest_dir
    lc_src = "lc-sb/"
    msu_src = "msu-sb/"
    dest_dir = "new-sb/"
    merge.merge_corpora(BASE_DIR, lc_src, msu_src, dest_dir)

    print("\nMapping acts from DAMSL to to smaller set:")
    file_dir = dest_dir
    map_acts.map_from_dml(BASE_DIR, file_dir)

    # print("\nClassifying sentences:")
    # model_dir = "/home/chas/Projects/Switchboard/cabnc/"
    # sentence_classification.classify_sentences(BASE_DIR, model_dir, file_dir)

    print("\nCreating .csvs from .chas:")
    cha_to_csv.convert_cha_to_csv(BASE_DIR, file_dir)

    print("\nAdding FTOs:")
    add_fto.add_ftos(BASE_DIR, file_dir)


if __name__ == "__main__":
    data_pipeline()
