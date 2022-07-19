# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-19 14:21:28
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-19 14:22:47

from datasets import load_dataset


def load_daily_dialog():
    dataset = load_dataset('daily_dialog')
    return dataset