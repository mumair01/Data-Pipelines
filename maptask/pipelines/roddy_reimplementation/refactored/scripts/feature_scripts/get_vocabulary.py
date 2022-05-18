# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-05-13 09:10:14
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-13 09:32:55

import os
import nltk
import pickle
import json
import xml.etree.ElementTree


def get_vocabulary_from_file(processed_gemaps_path, timed_unit_path):
    assert os.path.isfile(processed_gemaps_path)
    assert os.path.isfile(timed_unit_path)
    tree = xml.etree.ElementTree.parse(timed_unit_path).getroot()
    words_from_annotations = []
    for annotation_type in tree.findall('tu'):
        target_word = annotation_type.text.strip()
        if "--" in target_word:
            target_word = '--disfluency_token--'
            words_from_annotations.append(target_word)
        else:
            target_words = nltk.word_tokenize(target_word)
            words_from_annotations.extend(target_words)
    return words_from_annotations
