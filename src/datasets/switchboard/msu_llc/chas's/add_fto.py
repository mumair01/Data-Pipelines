"""
add_fto.py inserts the floor transfer offset as another column in the csv

The floor transfer offset (FTO) is a common measurement in conversation
analysis. It measures the timing bias between the end of one turn and the
start of the next. It only applies when the floor transfers --- that is
another person starts speaking. So, it has only been added to final turn
construction units (TCUs) in the csv data.

We've chosen to add it to the final TCU rather than the first TCU somewhat
arbitrarily, since it doesn't properly belong to either turn (it is the gap
between them. All times are in milliseconds.
"""

import os

def add_ftos(base_dir, file_dir):
    """ Add ftos for all files in the `file_dir` withing `base_dir`

    FTOs occur when there is a speaker change at the end of an utterance.
    So only utterances followed by a speaker change will include an FTO.
    """

    file_list = [x for x in os.listdir(base_dir + file_dir) if ".csv" in x]

    total = len(file_list)

    for i, file_name in enumerate(file_list):
        print(f"Updating {i+1} of {total}\t{file_name}")

        with open(base_dir + file_dir + file_name, 'r',
                  encoding="UTF-8") as input_file:
            lines = input_file.readlines()

        output = ""
        prev_speaker = ""
        prev_line = None
        prev_end = None

        header = True

        for line in lines:
            if header:
                output += f"{line.strip()},fto\n"
                header = False
                continue

            split_line = line.split(',')
            speaker = split_line[0]
            start = split_line[2]
            end = split_line[3]

            if speaker == prev_speaker:
                fto = ""
            else:
                try:
                    fto = int(start) - int(prev_end)
                except  ValueError:
                    fto = ""
                except TypeError:
                    fto = "fto"

            try:
                if not prev_line is None:
                    output += f"{prev_line.strip()},{fto}\n"
            except NameError:
                pass

            prev_line = line
            prev_speaker = speaker
            prev_end = end

        output += f"{prev_line.strip()},\n"

        with open(base_dir + file_dir + file_name, 'w',
                  encoding="UTF-8") as output_file:
            output_file.write(output)
