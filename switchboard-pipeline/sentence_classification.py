"""
sentence-classification.py uses a trained machine-learning model in
order to tag the syntax of each utterance in the corpus.

The script for training the model is given in cabnc/train_sentence_tagger.py.

Once the model has been trained, this file takes the .cha files from merge.py
(or map_acts.py, these can be done in either order), finds the words in each
utterance and uses the syntax classification model to add syntax annotations.

Each annotation (%dec, %int, %imp, and %non) is a probability of being in that
syntactic category (declarative, interrogative, imperative, and non-syntactic).
The raw model outputs numbers that must be put through the softmax function,
which is included in the script so that the final outputs are interpretable
probabilities.

See https://deepai.org/machine-learning-glossary-and-terms/softmax-layer
for information about the softmax function (lines 59-65).
"""

import os
import re
from math import exp

from transformers import AutoTokenizer, AutoModelForSequenceClassification


def classify_sentences(base_dir, model_dir, file_dir):
    """ Given the directories of the files and sentence classification model,
    append sentence type classifications to all utterances within the
    files in the directory."""

    tokenizer = AutoTokenizer.from_pretrained(model_dir,
                                              TOKENIZERS_PARALLELISM=False)
    model = AutoModelForSequenceClassification.from_pretrained(model_dir,
                                                               num_labels=4)

    file_list = [x for x in os.listdir(base_dir + file_dir) if ".cha" in x]

    total = len(file_list)
    count = 1

    for file_name in file_list:
        print(f"Updating {count} of {total}\t{file_name}")

        with open(base_dir+file_dir+file_name, 'r', encoding="UTF-8") as \
             cha_file:
            lines = cha_file.readlines()

        output = ""
        for line in lines:
            output += f"{line}"
            try:
                if re.match("\*[A-Z]{3}:", line):
                    line_input = " ".join(line.split()[1:])
                    inputs = tokenizer(line_input, return_tensors="pt")
                    outputs = model(**inputs)
                    # Use softmax to get probabilities
                    declarative = exp(outputs.logits[0][0])
                    interrogative = exp(outputs.logits[0][1])
                    imperative = exp(outputs.logits[0][2])
                    ungrammatical = exp(outputs.logits[0][3])
                    denom = declarative + interrogative + imperative + \
                        ungrammatical
                    # Check in to soft-labels
                    output += f"%dec:\t{declarative / denom}\n"
                    output += f"%int:\t{interrogative / denom}\n"
                    output += f"%imp:\t{imperative / denom}\n"
                    output += f"%non:\t{ungrammatical / denom}\n"
            except RuntimeError:
                pass

        with open(base_dir+file_dir+file_name, 'w',
                  encoding="UTF-8") as output_file:
            output_file.write(output)

        with open(base_dir + file_dir + file_name, 'r',
                  encoding="UTF-8") as output_file:
            lines = output_file.readlines()

        output = ""
        for line in lines:
            if not line.strip() == "":
                output += line

        with open(base_dir+file_dir+file_name, 'w',
                  encoding="UTF-8") as output_file:
            output_file.write(output)

        count += 1
