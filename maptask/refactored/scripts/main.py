# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-05-11 15:12:41
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-05-12 18:21:40

from corpus_scripts.maptask import MapTask
from pipeline import MapTaskPipelineSkantze


def execute_pipeline():
    maptask: MapTask = MapTask(
        load_dir="./dataset",
        audio_wget_script_path="/Users/muhammadumair/Documents/Repositories/mumair01-repos/Data-Pipelines/maptask/refactored/sh/maptaskBuild-12410-Mon-May-9-2022.wget.sh",
        corpus_subset=0.01
    )
    pipeline = MapTaskPipelineSkantze(maptask)
    pipeline.run(
        output_dir="./pipeline_results"
    )


if __name__ == "__main__":
    # Simply configure and run the pipeline here.
    execute_pipeline()
