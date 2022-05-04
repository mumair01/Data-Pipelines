"""
lc-cha converts Linguistic Consortium .utt files to .cha format

It's unclear where the .utt format comes from, but .cha is a standard
format used by the conversation analysis community. It has tooling built
around it for transcript markup at the utterance level, as well as
timing transcription. Also if timing is transcribed and the media files
are available, we can listen to the original media files in line with the
transcriptions when warranted. None of this is possible / desirable in the
.utt format.
"""

import sys
import re


def lc_to_cha(base_dir, dest_dir, da_file, convo_num):
    """ Given the base directory, destination director, source
    dialogue act file, and conversation number, write a .cha version
    of a transcript given by the Linguistic Consortium schema source."""
    with open(da_file, 'r', encoding="UTF-8") as input_file:
        lines = input_file.readlines()

    cha_output = "@Begin\n"
    cha_output += "@Languages:\teng\n"
    cha_output += "@Participants:\tSPA SPA Unidentified, SPB SPB Unidentified\n"
    cha_output += "@ID:\teng|Switchboard_Corpus|SPA||unknown||Unidentified|||\n"
    cha_output += "@ID:\teng|Switchboard_Corpus|SPB||unknown||Unidentified|||\n"
    cha_output += "@New Episode\n"

    regexp = re.compile("utt[0-9]+:")

    for line in lines:
        if not regexp.search(line):
            continue

        split_line = line.split()
        act = split_line[0]
        if act is None:
            sys.exit(1)
        speaker = split_line[1].split('.')[0]    ## The letter from e.g. A.1

        words = []
        for word in split_line[3:]:
            if word[-1] != "-":
                # We will match abandoned words
                word = re.sub('-', ' ', word)
            word = re.sub('--', '', word)
            word = re.sub('#', '', word)
            word = re.sub('{[A-Z]', '', word)
            word = re.sub('<[a-zA-Z ]+?>', '', word)
            word = re.sub('\[\[[ a-zA-Z]+?\]\]', '', word)
            word = re.sub('[(),+/?.{}\[\]]', '', word)
            if not word.strip() == "":
                words.append(word.lower())

        joined_words = " ".join(words)
        cha_output += f"*SP{speaker}:\t{joined_words}\n"
        cha_output += f"%dml:\t{act}\n".format(act)

    cha_output += "@End"

    with open(base_dir + dest_dir + convo_num + ".cha", 'w',
              encoding="UTF-8") as output_file:
        output_file.write(cha_output)


if __name__ == "__main__":
    lc_to_cha("/home/chas/Projects/Speech-Act-Modeling/",
              "new-sb",
              "lc-sb2/sw_0001_4325.utt",
              4325)
