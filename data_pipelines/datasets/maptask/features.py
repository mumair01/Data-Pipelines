# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-12 15:52:16
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2023-05-23 09:53:10

##############################
# This script contains methods to extract various features from the maptask
# corpus that are specific to that corpus. For example, there are methods to
# extract voice activity annotations / pause annotations directly from this
# corpus but no methods for speech features that are generalized
#  (e.g., pitch etc).
# TODO: This needs to be removed i.e., it is specific to the Skantze TRP
# models.
##############################

import os
import sys
import xml
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder

from data_pipelines.datasets.maptask.utils import *


################################# GLOBALS ####################################

# -- Voice activity defaults
DEFAULT_MINIMUM_VA_CLASSIFICATION_TIME_MS = 25
DEFAULT_FRAME_STEP_SIZE = 50
DEFAULT_VOICE_ACTIVITY_LABEL = 1


# -- Parts of speech  defaults
DEFAULT_POS_DELAY_TIME_MS = (
    100  # Assume that each POS calculation is delayed by 100ms.
)

################################# METHODS ####################################


def get_voice_activity_annotations(
    maptask_root_path,
    dialogue,
    participant,
    minimum_va_classification_time_ms=DEFAULT_MINIMUM_VA_CLASSIFICATION_TIME_MS,
    frame_step_size=DEFAULT_FRAME_STEP_SIZE,
    voice_activity_label=DEFAULT_VOICE_ACTIVITY_LABEL,
) -> pd.DataFrame:
    """
    Obtain the voice activity annotations from the maptask corpus using the
    given minimum classification time and step size.
    """
    va_times = get_utterance_times(maptask_root_path, dialogue, participant)
    # The last va time is the audio end time.
    audio_end_time_ms = va_times[-1][1] * 1000
    # Get only the VA values that are minimum length
    va_times = [
        va_time
        for va_time in va_times
        if va_time[1] - va_time[0] >= minimum_va_classification_time_ms / 1000
    ]
    # Get the frame times based on the final times unit time.
    # NOTE: This is being generated based on the step size for now.
    frame_times_s = np.arange(0, audio_end_time_ms, frame_step_size) / 1000
    # Array to store voice  activity - initially all zeros means no voice activity.
    voice_activity = np.zeros((frame_times_s.shape[0]))
    # Obtaining index relative to the frameTimes being considered for
    # which there is voice activity.
    for start_time_s, end_time_s in va_times:
        start_idx = np.abs(frame_times_s - start_time_s).argmin()
        end_idx = np.abs(frame_times_s - end_time_s).argmin()
        voice_activity[start_idx : end_idx + 1] = voice_activity_label
    # Ensure that there are no nan values introduced in the data.
    assert (
        not np.isnan(voice_activity).any() and not np.isnan(frame_times_s).any()
    )
    # TODO: Return as a numpy array only.
    return pd.DataFrame(
        {"frameTime": frame_times_s, "voiceActivity": voice_activity}
    )


def get_pos_annotations_with_delay(
    maptask_root_path,
    dialogue,
    participant,
    minimum_va_classification_time_ms=DEFAULT_MINIMUM_VA_CLASSIFICATION_TIME_MS,
    frame_step_size=DEFAULT_FRAME_STEP_SIZE,
    pos_delay_time_ms=DEFAULT_POS_DELAY_TIME_MS,
):
    va_times = get_utterance_times(maptask_root_path, dialogue, participant)
    # The last va time is the audio end time.
    audio_end_time_ms = va_times[-1][1] * 1000
    # Get only the VA values that are minimum length
    va_times = [
        va_time
        for va_time in va_times
        if va_time[1] - va_time[0] >= minimum_va_classification_time_ms / 1000
    ]
    # Get the frame times based on the final times unit time.
    # NOTE: This is being generated based on the step size for now.
    frame_times_s = np.arange(0, audio_end_time_ms, frame_step_size) / 1000
    # Obtain all the word pos annotations
    word_annotations = get_utterance_pos_annotations(
        maptask_root_path, dialogue, participant
    )
    # Generate mapping from pos tags to indices
    pos_tags_to_idx = {
        # NOTE: Indices start from 1 here because 0 already represents unknown categories.
        tag: i + 1
        for i, tag in enumerate(POS_TAGS)
    }
    # For all the collected word end times and POS tags, we need to introduce
    # a delay and add the POS annotation to the delayed frame.
    pos_annotations = np.zeros((frame_times_s.shape[0]))
    for end_time_s, pos_tag in word_annotations:
        frame_idx = np.abs(
            frame_times_s - (end_time_s + pos_delay_time_ms / 1000)
        ).argmin()
        # Convert to integer based on the vocabulary dictionary.
        pos_annotations[frame_idx] = pos_tags_to_idx[pos_tag]
    # The pos annotations should not have any nan values
    assert not np.isnan(pos_annotations).any()
    # This encoder will ignore any unknown tags by replacing them with all zeros.
    onehot_encoder = OneHotEncoder(sparse=False, handle_unknown="ignore")
    onehot_encoder.fit(
        np.asarray(list(pos_tags_to_idx.values())).reshape(-1, 1)
    )
    encoded_pos = onehot_encoder.transform(pos_annotations.reshape(-1, 1))
    pos_annotations_df = pd.DataFrame(encoded_pos, columns=POS_TAGS)
    # Add frametimes to the df
    pos_annotations_df.insert(0, "frameTime", frame_times_s)
    # Remove any duplicated frameTimes
    pos_annotations_df.drop_duplicates(subset=["frameTime"], inplace=True)
    assert not pos_annotations_df.isnull().values.any()
    # TODO: Return as a numpy array only.
    return pos_annotations_df
