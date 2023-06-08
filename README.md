# Data Pipelines

The data pipelines project allows users to load multiple datasets useful for
research in conversational AI, spoken dialogue systems, and linguistics.

It leverages the [transformers dataset infrastructure](https://huggingface.co/docs/datasets/quickstart)
to download and provide efficient access to variations of the same datasets -
maintaining a single copy of the raw data and using minimal disk space to store
dataset variations. Additionally, it provides access to a features package that can be used to extract commonly required features from these datasets (e.g., voice activity).

The goal is to abstract the process of loading datasets that are useful for
conversation research and allow researchers to focus on model development. It
is unique because it provides access to tools and variations of datasets that
might not be publicly available.

## In this README

- [Getting Started](#getting-started)
- [Basic Usage](#basic-usage)
- [Datasets and Variants](#datasets-and-variants)
  - [Callfriend](#callfriend)
  - [Callhome](#callhome)
  - [Fisher](#fisher)
  - [Maptask](#maptask)
  - [Switchboard](#switchboard)
- [Features Sub-package](#features-package)
- [Acknowledgements]()

## Getting Started


**IMPORTANT**: This repository only works on the i386 architecture on Mac OSX, not the arm64 architecture used in the newer Macs. 

The first step is to install data pipelines as a python package that can be
imported in python scripts. There is no pypi registry for this project.
Instead, it can be directly installed from Github as a package using pip.

Installations instructions for pip can be found [here](https://pip.pypa.io/en/stable/cli/pip_install/).

```bash
pip install git+https://github.com/mumair01/Data-Pipelines.git
```

Verify that the package has been installed using ipython:

```bash
ipython
```

```python
import data_pipelines
```

To install in developer mode, install the dev dependencies using:
```bash
pip install git+https://github.com/mumair01/Data-Pipelines.git '.[dev]'
```

## Basic Usage

This package provides two sub-packages: datasets and features. The datasets sub-package contains methods for loading and manipulating datasets, while the features sub-package provides more advanced feature extraction methods (e.g, audio feature extraction using OpenSmile).  


The DataPipeline class provides all methods required to access datasets. Datasets can loaded using the load_data method by specifying the name of the dataset, the variant, and any required keyword arguments.

```python
from data_pipelines.datasets import DataPipeline

dp = DataPipeline()
dset = dp.load_data(
    dataset=<DATASET_NAME>,
    variant=<DATASET_VARIANT,
    **kwargs
)
```

**NOTE:** The names of all datasets and variants are lowercase.

In the above example, ```<DATASET NAME>``` and ```<DATASET VARIANT>``` may be replaced
with the name of the dataset and its variant. Additionally, each dataset variant
expects its own keyword arguments. A summary is provided [here](#datasets-and-variants).

## Datasets and Variants

Data pipelines provides access to the following datasets and variants:

<table>
    <tr>
        <td><b> Dataset Name </b></td>
        <td><b> Variations </b></td>
        <td><b> Specific Keyword Arguments </b></td>
    </tr>
    <tr>
        <td> <a href="#callfriend"><b>Callfriend</b></a> </td>
        <td>default, audio </td>
        <td>language</td>
    </tr>
    <tr>
        <td> <a href="https://ca.talkbank.org/access/CallHome/eng.html"><b>Callhome</b></a> </td>
        <td>default, audio </td>
        <td>language</td>
    </tr>
    <tr>
        <td> <a href="https://catalog.ldc.upenn.edu/LDC2004T19"><b>Fisher</b></a> </td>
        <td>default, audio</td>
        <td>data_dir</td>
    </tr>
    <tr>
        <td> <a href="https://groups.inf.ed.ac.uk/maptask/"><b>Maptask</b></a> </td>
        <td>default, audio</td>
        <td>-</td>
    </tr>
    <tr>
        <td> <a href="https://isip.piconepress.com/projects/switchboard/"><b>Switchboard</b></a> </td>
        <td>isip-aligned, swda, ldc-audio</td>
        <td>data_dir (only for ldc-audio)</td>
    </tr>
</table>

## Callfriend

The [Callfriend](https://ca.talkbank.org/access/CallFriend/) corpus consists of 60 unscripted telephone conversations, lasting between 5-30 minutes. The corpus also includes documentation describing speaker information (sex, age, education, callee telephone number) and call information (channel quality, number of speakers).

This dataset accepts the following keyword arguments:

---
| Keyword     | Available values |
| ----------- | ----------- |
| language      | deu, eng-n, eng-s, fra-q, jpn, spa-c, spa, zho-m, zho-t       |
---

### Callfriend - Default variant

This variant provides access to the text features of the dataset including a unique id per conversation and a list of utterances with the speaker, start time, and time, and text, in the format specified below.

```python
_DEFAULT_FEATURES = {
    "id" : Value('string'),
    "utterances" : [{
            "speaker" : Value("string"),
            "start" : Value("float"),
            "end" : Value("float"),
            "text" : Value("string"),
        }
    ],
}
```

This variant is automatically downloaded if it does not exist at runtime.

### Callfriend - Audio variant

This variant provides access to the raw audio per conversation. It features a unique id per conversation and a path to the downloaded audio. It is recommended that users copy the audio if it will be modified.

The goal of this library is to provide general and efficient access to datasets. Therefore, we first provide only audio paths. Any features that are extracted may be added to the dataset and saved for efficient usage.

```python
_AUDIO_FEATURES = {
    "id" : Value('string'),
    "path" : Value("string"),
}
```

This variant is automatically downloaded if it does not exist at runtime.

## Callhome

The [Callhome](https://catalog.ldc.upenn.edu/LDC97S42) corpus was developed by the Linguistic Data Consortium (LDC) and consists of 120 unscripted 30-minute telephone conversations between native speakers of English. All calls originated in North America; 90 of the 120 calls were placed to various locations outisde of North America, while the remaining 30 calls were made within North America. Most participants called family members or close friends.

This dataset accepts the following keyword arguments:

---
| Keyword     | Available values |
| ----------- | ----------- |
| language      | ara, deu, eng, jpn, spa, zho    |
---

### Callhome - Default Variant

This variant provides access to the text features of the dataset including a unique id per conversation and a list of utterances with the speaker, start time, and time, and text, in the format specified below.

```python
_DEFAULT_FEATURES = {
    "id" : Value('string'),
    "utterances" : [{
            "speaker" : Value("string"),
            "start" : Value("float"),
            "end" : Value("float"),
            "text" : Value("string"),
        }
    ],
}
```

This variant is automatically downloaded if it does not exist at runtime.

### Callhome - Audio Variant

This variant provides access to the raw audio per conversation. It features a unique id per conversation and a path to the downloaded audio.

```python
_AUDIO_FEATURES = {
    "id" : Value('string'),
    "path" : Value("string"),
}
```

This variant is automatically downloaded if it does not exist at runtime.

## Fisher

The [Fisher](https://catalog.ldc.upenn.edu/LDC2004T19) English Training Speech Part 1 Transcripts was developed by the Linguistic Data Consortium (LDC) and contains time-aligned transcript data for 5,850 telephone conversations (984 hours) in English. In addition to the transcriptions, there is a complete set of tables describing the speakers, the properties of the telephone calls, and the set of topics that were used to initiate the conversations.

Note that due to licensing, any variant of the switchboard corpus **cannot** be downloaded automatically.

---
| Keyword     | Available values |
| ----------- | ----------- |
| data_dir     | Absolute path to the downloaded data directory   |
---

### Fisher- Default Variant

This variant provides access to the text features of the dataset including a unique session per conversation and a list of utterances with the speaker, start time, and time, and text, in the format specified below.

Before use, please download the transcripts [here]("https://catalog.ldc.upenn.edu/LDC2004T19").

```python
_DEFAULT_FEATURES = {
    "session" : Value('string'),
    "utterances" : [{
        "start" : Value("string"),
        "end" : Value('string'),
        "speaker" : Value('string'),
        "text" : Value('string')
    }]
}
```

### Fisher - Audio Variant

The variant provides access to the media from the corpus and includes a unique session and audio paths - including stereo audio, mono audio for speaker A, and mono audio for speaker B.

Before use, please download the media [here](""https://catalog.ldc.upenn.edu/LDC2004T19"").

```python
_AUDIO_FEATURES = {
    "session" : Value('string'),
    "audio_paths" : {
        "stereo" : Value('string'),
        "A" : Value('string'),
        "B" : Value('string')
    }
}
```

## Maptask

The [HCRC Map Task](https://groups.inf.ed.ac.uk/maptask/) Corpus is a set of 128 dialogues that has been recorded, transcribed, and annotated for a wide range of behaviours, and has been released for research purposes. It was originally designed to elicit behaviours that answer specific research questions in linguistics. You can read more about the design here. Since the original material was released in 1992, the corpus design has been used not just for linguistics research, but also in teaching and by computational linguists for training machine classifiers.

### MapTask - Default Variant

This variant provides access to the transcripts of the MapTask corpus. Each data item has a unique dialogue value, the participant value (follower or giver), and a list of utterances with the start time, end time, text, and part of speech.

This variant is automatically downloaded if it does not exist at runtime.

```python
_DEFAULT_FEATURES = {
    "dialogue" : Value("string"),
    "participant" : Value("string"),
    "utterances" : [{
            "start" : Value("float"),
            "end" : Value("float"),
            "text" : Value("string"),
            "pos" : Value("string")
        }
    ],
}
```

### MapTask - Audio Variant

This variant provides access to the audio of the MapTask corpus. It provides the dialogue value, the participant value, the stereo audio path, and the mono audio for the specified participant.

This variant is automatically downloaded if it does not exist at runtime.

```python
_AUDIO_FEATURES = {
    "dialogue" : Value("string"),
    "participant" : Value("string"),
    "audio_paths" : {
        "stereo" : Value("string"),
        "mono" : Value("string"),
    },
}
```

## Switchboard

The [Switchboard corpus](https://isip.piconepress.com/projects/switchboard/), consisting of telephone conversations between speakers of American English, is one of the longest-standing corpora of fully spontaneous speech. As such, there have been a range of different sorts of linguistic information annotated on it, including syntax, discourse semantics and prosody

### Switchboard - isip-aligned variant

This variant provides access to the switchboard transcripts that were aligned by [isip]("https://isip.piconepress.com/projects/switchboard/") and released on 10/19/02. It provides a unique session value, a participant value, and a list of turns. Each turn item consists of the start time, end time, text, and a list of tokens. Each token contains the words that make up the turn, including their individual start and end times.

This variant is automatically downloaded if it does not exist at runtime.

```python
features={
    "session" : Value("string"),
    "participant" : Value("string"),
    "turns" : [{
        "start" : Value('float'),
        "end" : Value("float"),
        "text" : Value("string"),
        "tokens" : [{
            "start" : Value('float'),
            "end" : Value("float"),
            "text" : Value("string"),
        }]
    }]
},
```

### Switchboard - swda variant

The Switchboard Dialog Act Corpus (SwDA) extends the Switchboard-1 Telephone Speech Corpus, Release 2 with turn/utterance-level dialog-act tags. The tags summarize syntactic, semantic, and pragmatic information about the associated turn. The SwDA project was undertaken at UC Boulder in the late 1990s. The SwDA is not inherently linked to the Penn Treebank 3 parses of Switchboard, and it is far from straightforward to align the two resources. In addition, the SwDA is not distributed with the Switchboard's tables of metadata about the conversations and their participants.

Further description can be found [here](https://huggingface.co/datasets/swda).

This variant is automatically downloaded if it does not exist at runtime.

### Switchboard - ldc-audio variant

This variant provides access to the audio of the switchboard corpus.

Before use, please download the media [here](""https://catalog.ldc.upenn.edu/LDC2004T19"") and specify absolute path using data_dir.

```python
 features={
    "session" : Value('string'),
    "participant" : Value('string'),
    "audio_paths" : {
        "stereo" : Value('string'),
        "mono" : Value('string')
    },
},
```

## Features Package

The goal of this project is to be able to easily download and parse commonly used dataset in Conversational AI research. The ```load_dataset``` method describes in previous methods provides access to common features for each dataset. However, depending on the application, there may be a need to extract additional features. For example, audio feature sets (such as GeMAPS) may be required - or voice activity from the transcripts may be required.

The Features sub-package provides access to methods that may be used for these purposes. The goal is to map these methods on the dataset and save them for efficient access later.

**NOTE:** Further documentation is forthcoming.


## Acknowledgements

Developed by [Muhammad Umair](https://www.linkedin.com/in/mumair/) at the [Human Interaction Lab](https://sites.tufts.edu/hilab/) at Tufts University, Medford, MA. 
 
This project uses the [transformers library](https://aclanthology.org/2020.emnlp-demos.6/)
and was inspired by Erik's [datasets_turntaking project](https://github.com/ErikEkstedt/datasets_turntaking).
