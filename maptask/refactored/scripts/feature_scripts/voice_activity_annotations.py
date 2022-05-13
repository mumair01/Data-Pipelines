# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-05-12 18:23:32
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-12 19:36:30

import os
import pandas as pd
import numpy as np
import xml.etree.ElementTree

# Minimum size of a detection for potential voice activity.
MINIMUM_DETECTION_MS = 0.025


def extract_voice_activity_labels(raw_genome_file_path, timed_unit_path, output_dir):
    assert os.path.isdir(output_dir)
    assert os.path.isfile(raw_genome_file_path)
    assert os.path.isfile(timed_unit_path)
    frame_times = np.array(
        pd.read_csv(raw_genome_file_path, delimiter=",", usecols=[1])['frameTime'])
    voice_activity = np.zeros((len(frame_times)))
    tree = xml.etree.ElementTree.parse(timed_unit_path).getroot()
    # Obtain the annotation data first.
    annotation_data = []
    for annotation_type in tree.findall('tu'):
        annotation_data.append(
            (float(annotation_type.get('start')),
                float(annotation_type.get('end'))))
    # Remove any detections that are less than 90ms.
    # TODO: Determine why this is the case / why do this step.
    annotation_data = [data for data in annotation_data
                       if data[1] - data[0] >= MINIMUM_DETECTION_MS]
    # Only obtain the frames that contain voice activity for at least X%
    # of duration
    # TODO: Not sure how this is currently getting X% for VAD in frame.
    for start_frame, end_frame in annotation_data:
        start_idx = (np.abs(frame_times-start_frame)).argmin()
        end_idx = (np.abs(frame_times - end_frame)).argmin()
        voice_activity[start_idx: end_idx+1] = 1
    # Output the results
    output = pd.DataFrame([frame_times, voice_activity])
    output = np.transpose(output)
    output.columns = ['frameTimes', 'vad']
    filename = os.path.splitext(os.path.basename(raw_genome_file_path))[0]
    output.to_csv(os.path.join(output_dir, "{}.csv".format(
        filename)), float_format='%.6f', sep=',', index=False, header=True)
