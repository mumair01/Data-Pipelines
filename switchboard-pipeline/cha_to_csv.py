"""
cha_to_csv.py converts .cha files to .csv files

.cha files are the most common format for conversation analysis, but
they are not amenable to computational work. Instead, we use csv files
which should be easily importable into any computational system.
"""

import os
import re

def convert_cha_to_csv(base_dir, file_dir):
    """ Given the base directory and file directory within,
    create .csv files for each .cha file present."""
    file_list = [x for x in os.listdir(base_dir + file_dir) if ".cha" in x]

    total = len(file_list)

    for count, file_name in enumerate(file_list):
        print(f"Updating {count+1} of {total}\t{file_name}")

        with open(base_dir+file_dir+file_name, 'r',
                  encoding="UTF-8") as input_file:
            lines = input_file.readlines()

        headings = ["speaker", "words", "start", "end", "declarative", "interrogative",
                    "imperative", "non-syntactic", "damsl", "swbd_damsl", "function"]

        utt_dict = {}

        annotation_map = {"dec": "declarative",
                          "int": "interrogative",
                          "imp": "imperative",
                          "non": "non-syntactic",
                          "dml": "damsl",
                          "swb": "swbd_damsl",
                          "fun": "function"}

        output = ",".join(headings)
        output += "\n"

        for line in lines:
            if re.match("\*[A-Z]{3}:", line):
                if not len(utt_dict.keys()) == 0:
                    for heading in headings:
                        try:
                            if utt_dict[heading] == '"':
                                ## For the " damsl annotation so that it doesn't
                                ## mess up the csv readers, we escape the char.
                                output += '\\",'
                            else:
                                output += f"{utt_dict[heading]},"
                        except KeyError:
                            output += ","
                    output = output[:-1]
                    output += "\n"
                utt_dict = {}
                utt_dict["speaker"] = line.split(":")[0][1:]
                try:
                    timestamps = line.split("•")[1]
                    utt_dict["start"] = timestamps.split("_")[0]
                    utt_dict["end"] = timestamps.split("_")[1]
                    utt_dict["words"] = line.split("•")[0].split("\t")[1].strip()
                except IndexError:
                    utt_dict["start"] = ""
                    utt_dict["end"] = ""
                    utt_dict["words"] = line.split(":")[1].strip()
            if re.match("%[a-z]{3}:", line):
                annotation = line[1:4]
                utt_dict[annotation_map[annotation]] = line.split()[1]

        if not len(utt_dict.keys()) == 0:
            for heading in headings:
                try:
                    output += f"{utt_dict[heading]},"
                except KeyError:
                    output += ","
            output = output[:-1]

        with open(base_dir+file_dir+file_name.split(".")[0]+".csv", 'w',
                  encoding="UTF-8") as output_file:
            output_file.write(output)

if __name__ == "__main__":
    convert_cha_to_csv("/home/chas/Projects/Switchboard/", "new-sb/")
