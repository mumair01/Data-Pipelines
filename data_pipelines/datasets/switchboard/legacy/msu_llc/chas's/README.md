
# Table of Contents

1.  [The Switchboard Corpus](#orgfa1e71b)
    1.  [MSU Switchboard Transcripts](#org71dd4e4)
        1.  [Word Level Transcripts](#orge5a59cb)
        2.  [Utterance Level Transcripts](#orgca16725)
        3.  [Processed Utterance Transcripts](#org7bd06da)
        4.  [CHAT Transcripts](#org1e6d4e7)
    2.  [Linguistic Consortium Transcripts](#org415c9c1)
        1.  [Penn Treebank Corpus](#org687bb58)
        2.  [CHAT Transcripts](#org4cd93b0)
2.  [Data Transformations](#orgd8d406c)
    1.  [Data Cleaning and Formatting Pipeline](#org90e7859)
    2.  [Dialogue Acts](#org0650842)


<a id="orgfa1e71b"></a>

# The Switchboard Corpus

[The Switchboard Corpus](https://catalog.ldc.upenn.edu/LDC97S62) is a collection of telephone conversations collected in 1992-1993. It consists of about 2400 conversations between 543 speakers. Participants were auto-dialed and given one of 70 prerecorded prompts. No two participants spoke to each other more than once and no participant had the same subject prompt twice.


<a id="org71dd4e4"></a>

## [MSU Switchboard Transcripts](http://www.openslr.org/5/)

Mississippi State has transcribed the Switchboard corpus with word- and utterance-level timing. Each file is listed as `swNNNNP-ms98-a-TYPE.text` where:

-   `NNNN` is the conversation number
-   `P` is either "A" or "B" for the participant channel
-   `TYPE` is either word or trans for the transcription level. MSU claims transcription word error rates below 1%.


<a id="orge5a59cb"></a>

### Word Level Transcripts

Word level transcripts are space separated with the following format:

    swNNNNP-ms98-a-XXXX S.SSSSSS E.EEEEEE WORD

-   `NNNN` is the conversation number, matching the filename.
-   `P` is the participant A or B, matching the filename.
-   `XXXX` is the word number, counting from 1.
-   `S.SSSSSS` is the timing of the beginning of the word to the eighth of a millisecond
-   `E.EEEEEE` is the timing of the end of the word to the eighth of a millisecond
-   `WORD` is the word being transcribed. Non-words are fully bracketed &#x2014; [noise]. Abandoned words are bracketed and given a hyphen &#x2014; "an[y]-"

We've found word level timing to be generally reliable, though care should be taken in applying them widely.


<a id="orgca16725"></a>

### Utterance Level Transcripts

Utterance level transcripts are space separated with the following format:

    swNNNNP-ms98-a-XXXX S.SSSSSS E.EEEEEE WORD...

-   `NNNN` is the conversation number, matching the filename.
-   `P` is the participant A or B, matching the filename.
-   `XXXX` is the utterance number, counting from 1.
-   `S.SSSSSS` is the timing of the beginning of the utterance to the eighth of a millisecond.
-   `E.EEEEEE` is the timing of the end of the utterance to the eighth of a millisecond.
-   `WORD...` is series of words being transcribed. Non-words are fully bracketed &#x2014; [noise]. Abandoned words are bracketed and given a hyphen &#x2014; "an[y]-". Each utterance has one or more words, though "[silence]" is included in each transcript as an utterance.

Utterance timing is generally unreliable. It is unclear what the assumptions are, but both beginning and ending timing can be off by as much as a half-second from word timing.


<a id="org7bd06da"></a>

### Processed Utterance Transcripts

Since the utterance level timing was not sufficient for conversation level analysis, We've re-worked the original transcripts into a new set of transcripts that uses the word level timing, but the utterance-level transcriptions. These files are named in the `NNNN-P.csv` format, where: `NNNN` is the conversation number and `P` is the participant. The format was changed to `csv` for ease of importing data. The first row was also dropped, since it is implicit, as were the "[silence]" turns.

The code creating these files can be found in `re-time-msu.py`.


<a id="org1e6d4e7"></a>

### CHAT Transcripts

Transcripts in the `.cha` format for use with [CLAN](https://dali.talkbank.org/clan/) or ALAN are provided. These files are named `NNNN.cha` where `NNNN` is the conversation number. `.cha` is one standard for examining conversational data. These files were created with the `msu-chat.py` script.


<a id="org415c9c1"></a>

## [Linguistic Consortium Transcripts](https://web.stanford.edu/~jurafsky/ws97/)

These transcripts are the original markup for [Stolcke et al. 1998](https://www.aaai.org/Papers/Symposia/Spring/1998/SS-98-01/SS98-01-015.pdf). Details about the tagging schema can be found [in the online coders manual](https://web.stanford.edu/~jurafsky/ws97/manual.august1.html). The Switchboard corpus is coded in SWBD-DAMSL, which is an adaptation of the DAMSL scheme proposed in [Core and Allen 1997](http://www.justinecassell.com/discourse07/Week5Reading/Core_DAMSLannotation.pdf).


<a id="org687bb58"></a>

### [Penn Treebank Corpus](https://www.seas.upenn.edu/~pdtb/)

Dialogue act annotations were applied to the Penn Treebank transcriptions.

These transcripts can be found in the `lc-sb` folder. Within each folder, files have the format `sw_CCXX_YYYY.utt` where:

-   `CC` is the collection number
-   `XX` is the number within that collection
-   `YYYY` is the conversation ID number.

Each file has begins with copyright information and then header information with transcriber notes. The transcript begins after a line of `=` marks.

Each utterance is given in the following format:

    TAG       P.N uttC: WORDS... \n

Where:

-   `TAG` comes from the tag set in the documentation (see below for more)
-   `P` is either "A" or "B", matching the participant
-   `N` is the overall turn number for the conversation
-   `C` is the utterance number within the turn
-   `WORDS` are the transcription.

The tags in the transcriptions are chiefly from the [Coders Manual](https://web.stanford.edu/~jurafsky/ws97/manual.august1.html), but note that tags may be from clustered set, the Entire Label Set, the original 226 tags, or combination of multiple tags, as the called for in the [Core and Allen](http://www.justinecassell.com/discourse07/Week5Reading/Core_DAMSLannotation.pdf) paper proposing the `DAMSL` schema.

Words in the transcription are mostly word-level, but the transcripts also include markup of other sorts, such as "{D well, } [ they, +  {F uh, }" or "it seems to me <baby>  that [ it's, + it's ]". Work remains to be done about the semantics of this markup.


<a id="org4cd93b0"></a>

### CHAT Transcripts

Transcripts in the `.cha` format for use with [CLAN](https://dali.talkbank.org/clan/) or ALAN are provided. Follow the same naming scheme as above, but with a different suffix. `.cha` is one standard for examining conversational data, especially in conversation analysis. These files were produced with the `lc-cha.py` script.

These transcripts are also annotated with sentence type tagging from the model detailed below.


<a id="orgd8d406c"></a>

# Data Transformations


<a id="org90e7859"></a>

## Data Cleaning and Formatting Pipeline

As outlined above, our data comes from the Linguistic Consortium and Mississippi State University transcriptions of the Switchboard corpus. In order to get this data into a usable format for modeling, we've performed several transformations. The pipeline below will replicate this process:

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Script</th>
<th scope="col" class="org-left">Source</th>
<th scope="col" class="org-left">Destination</th>
<th scope="col" class="org-left">Output Format</th>
<th scope="col" class="org-left">Purpose</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">`re-utterizer.py`</td>
<td class="org-left">`lc-sb`</td>
<td class="org-left">`lc-sb`</td>
<td class="org-left">lc format</td>
<td class="org-left">Combine utterances marked as</td>
</tr>


<tr>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">continuations are combined with</td>
</tr>


<tr>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">the host utterance to complete it</td>
</tr>


<tr>
<td class="org-left">`merge.py`</td>
<td class="org-left">`lc-sb2`</td>
<td class="org-left">`new-sb`</td>
<td class="org-left">`.cha`</td>
<td class="org-left">Get the timing information from the</td>
</tr>


<tr>
<td class="org-left">&#xa0;</td>
<td class="org-left">`msu-sb`</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">MSU corpus and the dialogue acts</td>
</tr>


<tr>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">from the Linguistic Consortium</td>
</tr>


<tr>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">and pile them in together.</td>
</tr>


<tr>
<td class="org-left">`map_acts.py`</td>
<td class="org-left">`new-sb`</td>
<td class="org-left">`new-sb`</td>
<td class="org-left">`.cha`</td>
<td class="org-left">Adds swbd-damsl annotations and</td>
</tr>


<tr>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">function annotations according</td>
</tr>


<tr>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">to the table below.</td>
</tr>


<tr>
<td class="org-left">`cha_to_csv.py`</td>
<td class="org-left">`new-sb`</td>
<td class="org-left">`new-sb`</td>
<td class="org-left">`.csv`</td>
<td class="org-left">Convert `.cha` files to `.csv` files</td>
</tr>


<tr>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">for ease of computation</td>
</tr>


<tr>
<td class="org-left">`add_fto.py`</td>
<td class="org-left">`new-sb`</td>
<td class="org-left">`new-sb`</td>
<td class="org-left">`.csv`</td>
<td class="org-left">Add column for Floor Transfer Offset</td>
</tr>


<tr>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">for turns before floor transfer</td>
</tr>
</tbody>
</table>

There are also a few extra scripts that are not a part of the master pipeline. They may be useful for other work, like examining the files where the transcripts are too different to use both timing and dialogue act information

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Script</th>
<th scope="col" class="org-left">Source</th>
<th scope="col" class="org-left">Destination</th>
<th scope="col" class="org-left">Output Format</th>
<th scope="col" class="org-left">Purpose</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">`lc_cha.py`</td>
<td class="org-left">`lc-sb2`</td>
<td class="org-left">`lc-cha`</td>
<td class="org-left">`.cha`</td>
<td class="org-left">Converts Linguistic Consortium transcripts</td>
</tr>


<tr>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">to the `.cha` format</td>
</tr>
</tbody>
</table>


<a id="org0650842"></a>

## Dialogue Acts

The Linguistic Consortium corpus is tagged according to the [the annotation manual](https://web.stanford.edu/~jurafsky/ws97/manual.august1.html), but was done by hand. So the data is a bit messy. By scraping the data, we come up with the following list of unique tags in the corpus along with the number of times each tag occurs in the corpus. The `description` is the human-readable description according to the annotation manual. Many of the tags are combinations of documented annotations or errors in the annotations, so the data here differs somewhat from the annotation manual. The '+', '@', and '\*' annotations have been cleaned out in the transcripts in `lc-sb2`. These are continuations, which have been merged with the rest of their utterance units; segmentation errors, which we have not fixed except where the segmentation errors co-occur with continuation annotations; and transcription errors, which are not useful unless we begin modeling at a word level.

Jurafsky et al. clustered the annotations according to the schema noted in the manual. The mapping is given below.

See [Threlkeld & de Ruiter, 2022](./literature/Threlkeld_de_Ruiter.pdf) for an explanation of the current set of dialogue acts, and a brief discussion of possible extensions.

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-right" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">DAMSL Tag</th>
<th scope="col" class="org-right">Count</th>
<th scope="col" class="org-left">Cluster</th>
<th scope="col" class="org-left">Description</th>
<th scope="col" class="org-left">Mapping</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">sd</td>
<td class="org-right">70688</td>
<td class="org-left">sd</td>
<td class="org-left">Statement-non-opinion</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">b</td>
<td class="org-right">36304</td>
<td class="org-left">b</td>
<td class="org-left">Acknowledge (Backchannel)</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">sv</td>
<td class="org-right">25805</td>
<td class="org-left">sv</td>
<td class="org-left">Statement-opinion</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">%</td>
<td class="org-right">15611</td>
<td class="org-left">%</td>
<td class="org-left">Abandoned or Turn-Exit</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">aa</td>
<td class="org-right">10172</td>
<td class="org-left">aa</td>
<td class="org-left">Agree/Accept</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">ba</td>
<td class="org-right">4536</td>
<td class="org-left">ba</td>
<td class="org-left">Appreciation</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">qy</td>
<td class="org-right">3807</td>
<td class="org-left">qy</td>
<td class="org-left">Yes-No-Question</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">x</td>
<td class="org-right">3653</td>
<td class="org-left">x</td>
<td class="org-left">Non-verbal</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">ny</td>
<td class="org-right">2839</td>
<td class="org-left">ny</td>
<td class="org-left">Yes Answers</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">fc</td>
<td class="org-right">2404</td>
<td class="org-left">fc</td>
<td class="org-left">Conventional-Closing</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">b<sup>r</sup></td>
<td class="org-right">2126</td>
<td class="org-left">b</td>
<td class="org-left">Acknowledge Self-Repeat</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">sd<sup>e</sup></td>
<td class="org-right">1952</td>
<td class="org-left">sd</td>
<td class="org-left">Statement Expansions of y/n Answers</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">qw</td>
<td class="org-right">1895</td>
<td class="org-left">qw</td>
<td class="org-left">Wh-Question</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">sd(<sup>q</sup>)</td>
<td class="org-right">1342</td>
<td class="org-left">sd</td>
<td class="org-left">Statement w/ Quotation</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">bk</td>
<td class="org-right">1257</td>
<td class="org-left">bk</td>
<td class="org-left">Response Acknowledgement</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">nn</td>
<td class="org-right">1235</td>
<td class="org-left">nn</td>
<td class="org-left">No Answers</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">qy<sup>d</sup></td>
<td class="org-right">1229</td>
<td class="org-left">qy<sup>d</sup></td>
<td class="org-left">Declarative Yes-No-Question</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">h</td>
<td class="org-right">1222</td>
<td class="org-left">h</td>
<td class="org-left">Hedge</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">bh</td>
<td class="org-right">1048</td>
<td class="org-left">bh</td>
<td class="org-left">Backchannel in Question Form</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">^q</td>
<td class="org-right">972</td>
<td class="org-left">^q</td>
<td class="org-left">Quotation</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">bf</td>
<td class="org-right">941</td>
<td class="org-left">bf</td>
<td class="org-left">Summarize/reformulate</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sd<sup>t</sup></td>
<td class="org-right">930</td>
<td class="org-left">sd</td>
<td class="org-left">Statement about Task</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">aa<sup>r</sup></td>
<td class="org-right">918</td>
<td class="org-left">aa</td>
<td class="org-left">Agree/Accept Repeat</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">+@</td>
<td class="org-right">867</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">Continuation w/ error</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">o</td>
<td class="org-right">804</td>
<td class="org-left">bc</td>
<td class="org-left">Other</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">na</td>
<td class="org-right">768</td>
<td class="org-left">na</td>
<td class="org-left">Affirmative Non-Yes Answer</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">^2</td>
<td class="org-right">715</td>
<td class="org-left">^2</td>
<td class="org-left">Collaborative Completion</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">b<sup>m</sup></td>
<td class="org-right">694</td>
<td class="org-left">b<sup>m</sup></td>
<td class="org-left">Repeat Phrase</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">ad</td>
<td class="org-right">674</td>
<td class="org-left">ad</td>
<td class="org-left">Action Directive</td>
<td class="org-left">Command</td>
</tr>


<tr>
<td class="org-left">qo</td>
<td class="org-right">644</td>
<td class="org-left">qo</td>
<td class="org-left">Open-ended Question</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qh</td>
<td class="org-right">565</td>
<td class="org-left">qh</td>
<td class="org-left">Rhetorical Question</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">^h</td>
<td class="org-right">553</td>
<td class="org-left">^h</td>
<td class="org-left">Hold before answer/agreement</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">qy<sup>g</sup></td>
<td class="org-right">436</td>
<td class="org-left">qy</td>
<td class="org-left">Tag question</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">o@</td>
<td class="org-right">339</td>
<td class="org-left">bc</td>
<td class="org-left">Overloaded TCU</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">ar</td>
<td class="org-right">303</td>
<td class="org-left">ar</td>
<td class="org-left">Reject</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sv(<sup>q</sup>)</td>
<td class="org-right">301</td>
<td class="org-left">sv</td>
<td class="org-left">Statement-Opinion w/ Quotation</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">ng</td>
<td class="org-right">291</td>
<td class="org-left">ng</td>
<td class="org-left">Negative Non-No Answers</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">no</td>
<td class="org-right">285</td>
<td class="org-left">no</td>
<td class="org-left">Other Answers</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sd<sup>r</sup></td>
<td class="org-right">248</td>
<td class="org-left">sd</td>
<td class="org-left">Statement, Self-repeat</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">br</td>
<td class="org-right">237</td>
<td class="org-left">br</td>
<td class="org-left">Signal Non-Understanding</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">sd@</td>
<td class="org-right">230</td>
<td class="org-left">sd</td>
<td class="org-left">Statement w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">qr</td>
<td class="org-right">221</td>
<td class="org-left">qy</td>
<td class="org-left">Or Question</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">fp</td>
<td class="org-right">209</td>
<td class="org-left">fp</td>
<td class="org-left">Conventional Opening</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">qrr</td>
<td class="org-right">199</td>
<td class="org-left">qrr</td>
<td class="org-left">Or-question tacked onto yes-no question</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">ny<sup>r</sup></td>
<td class="org-right">196</td>
<td class="org-left">ny</td>
<td class="org-left">Yes w/ repeat</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">nd</td>
<td class="org-right">181</td>
<td class="org-left">nd</td>
<td class="org-left">Dispreferred Answer</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sv<sup>t</sup></td>
<td class="org-right">159</td>
<td class="org-left">sv</td>
<td class="org-left">Opinion about task</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">nn<sup>r</sup></td>
<td class="org-right">137</td>
<td class="org-left">nn</td>
<td class="org-left">No Answer w/ repeat</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">fe</td>
<td class="org-right">136</td>
<td class="org-left">ba</td>
<td class="org-left">Exclamation</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">fc<sup>m</sup></td>
<td class="org-right">131</td>
<td class="org-left">fc</td>
<td class="org-left">Conventional Closing w/ mimic</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">%@</td>
<td class="org-right">130</td>
<td class="org-left">%</td>
<td class="org-left">Abandoned w/ error</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">sv<sup>e</sup></td>
<td class="org-right">118</td>
<td class="org-left">sv</td>
<td class="org-left">Opinion, expansion of y/n answer</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">t3</td>
<td class="org-right">117</td>
<td class="org-left">t3</td>
<td class="org-left">3rd Party Talk</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">qy<sup>t</sup></td>
<td class="org-right">115</td>
<td class="org-left">qy</td>
<td class="org-left">Yes/No Question about Task</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">t1</td>
<td class="org-right">104</td>
<td class="org-left">t1</td>
<td class="org-left">Self-talk</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">ba<sup>r</sup></td>
<td class="org-right">103</td>
<td class="org-left">ba</td>
<td class="org-left">Appreciation w/ repeat</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">bd</td>
<td class="org-right">96</td>
<td class="org-left">bd</td>
<td class="org-left">Downplayer</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">^g</td>
<td class="org-right">92</td>
<td class="org-left">^g</td>
<td class="org-left">Tag Question</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sv<sup>r</sup></td>
<td class="org-right">88</td>
<td class="org-left">sv</td>
<td class="org-left">Opinion w/ repeat</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sv@</td>
<td class="org-right">84</td>
<td class="org-left">sv</td>
<td class="org-left">Opinion w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">qw<sup>d</sup></td>
<td class="org-right">83</td>
<td class="org-left">qw<sup>d</sup></td>
<td class="org-left">Declarative wh-question</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">b@</td>
<td class="org-right">80</td>
<td class="org-left">b</td>
<td class="org-left">Backchannel w/ error</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">ft</td>
<td class="org-right">76</td>
<td class="org-left">ft</td>
<td class="org-left">Thanking</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">fa</td>
<td class="org-right">76</td>
<td class="org-left">fa</td>
<td class="org-left">Apology</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">aa<sup>m</sup></td>
<td class="org-right">70</td>
<td class="org-left">aa</td>
<td class="org-left">Accept w/ repeat</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">sd<sup>m</sup></td>
<td class="org-right">67</td>
<td class="org-left">sd</td>
<td class="org-left">Statement w/ mimic</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">ad<sup>t</sup></td>
<td class="org-right">64</td>
<td class="org-left">ad</td>
<td class="org-left">Action-directive about task</td>
<td class="org-left">Command</td>
</tr>


<tr>
<td class="org-left">br<sup>m</sup></td>
<td class="org-right">59</td>
<td class="org-left">br</td>
<td class="org-left">Signal Non-understanding w/ mimic</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">aap</td>
<td class="org-right">57</td>
<td class="org-left">am</td>
<td class="org-left">Accept Part</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">sd<sup>c</sup></td>
<td class="org-right">50</td>
<td class="org-left">sd</td>
<td class="org-left">Statement about communication</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">qw<sup>t</sup></td>
<td class="org-right">49</td>
<td class="org-left">qw</td>
<td class="org-left">Wh-question about task</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">co</td>
<td class="org-right">49</td>
<td class="org-left">cc</td>
<td class="org-left">Offer</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">x@</td>
<td class="org-right">48</td>
<td class="org-left">x</td>
<td class="org-left">Non-speech w/ error</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">sd\*</td>
<td class="org-right">46</td>
<td class="org-left">sd</td>
<td class="org-left">Statement w/ transcription error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">am</td>
<td class="org-right">44</td>
<td class="org-left">am</td>
<td class="org-left">Maybe</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">ar<sup>r</sup></td>
<td class="org-right">41</td>
<td class="org-left">ar</td>
<td class="org-left">Reject w/ repeat</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">na<sup>r</sup></td>
<td class="org-right">37</td>
<td class="org-left">na</td>
<td class="org-left">Affirmative non-yes w/ repeat</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">na<sup>m</sup></td>
<td class="org-right">35</td>
<td class="org-left">na</td>
<td class="org-left">Affirmative non-yes w/ mimic</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">cc</td>
<td class="org-right">35</td>
<td class="org-left">cc</td>
<td class="org-left">Commit</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">"</td>
<td class="org-right">35</td>
<td class="org-left">bc</td>
<td class="org-left">Other</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">ba@</td>
<td class="org-right">32</td>
<td class="org-left">ba</td>
<td class="org-left">Appreciation w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">bk<sup>r</sup></td>
<td class="org-right">30</td>
<td class="org-left">bk</td>
<td class="org-left">Acknowledge w/ repeat</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">qy<sup>r</sup></td>
<td class="org-right">29</td>
<td class="org-left">qy</td>
<td class="org-left">Yes-no Question w/ repeat</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">fc<sup>t</sup></td>
<td class="org-right">29</td>
<td class="org-left">fc</td>
<td class="org-left">Conventional Closing about task</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">sv<sup>m</sup></td>
<td class="org-right">25</td>
<td class="org-left">sv</td>
<td class="org-left">Opinion w/ mimic</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">+</td>
<td class="org-right">25</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">Segment</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">sv\*</td>
<td class="org-right">23</td>
<td class="org-left">sv</td>
<td class="org-left">Opinion w/ transcription Error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">arp</td>
<td class="org-right">23</td>
<td class="org-left">nd</td>
<td class="org-left">Dispreferred Answer</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sd(<sup>q</sup>)<sup>t</sup></td>
<td class="org-right">22</td>
<td class="org-left">sd</td>
<td class="org-left">Statement w/ quotation about task</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">qy<sup>h</sup></td>
<td class="org-right">21</td>
<td class="org-left">qy</td>
<td class="org-left">Yes-no Question hold before answer</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qy@</td>
<td class="org-right">21</td>
<td class="org-left">qy</td>
<td class="org-left">Yes-no Question w/ error</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">bk<sup>m</sup></td>
<td class="org-right">21</td>
<td class="org-left">bk</td>
<td class="org-left">Acknowledge Answer w/ mimic</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">aa@</td>
<td class="org-right">21</td>
<td class="org-left">aa</td>
<td class="org-left">Accept w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">qy<sup>g</sup><sup>t</sup></td>
<td class="org-right">19</td>
<td class="org-left">qy</td>
<td class="org-left">Yes-no Question Tag Question about Task</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">by</td>
<td class="org-right">19</td>
<td class="org-left">bc</td>
<td class="org-left">Sympathy</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">fc<sup>r</sup></td>
<td class="org-right">18</td>
<td class="org-left">fc</td>
<td class="org-left">Conventional Closing, repeat</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">sd,o@</td>
<td class="org-right">16</td>
<td class="org-left">sd</td>
<td class="org-left">Statement, other</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">qy<sup>m</sup></td>
<td class="org-right">16</td>
<td class="org-left">qy</td>
<td class="org-left">Yes-no question w/ mimic</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qy<sup>c</sup></td>
<td class="org-right">16</td>
<td class="org-left">qy</td>
<td class="org-left">Yes-no Question about communication</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">fp<sup>m</sup></td>
<td class="org-right">15</td>
<td class="org-left">fp</td>
<td class="org-left">Conventional Opening Mimic</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">qy<sup>d</sup><sup>t</sup></td>
<td class="org-right">14</td>
<td class="org-left">qy<sup>d</sup></td>
<td class="org-left">Declarative Yes-no question about task</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qw<sup>r</sup></td>
<td class="org-right">14</td>
<td class="org-left">qw</td>
<td class="org-left">Wh-question repeat</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qr<sup>d</sup></td>
<td class="org-right">13</td>
<td class="org-left">qy</td>
<td class="org-left">Declarative Or-question</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">co<sup>t</sup></td>
<td class="org-right">13</td>
<td class="org-left">cc</td>
<td class="org-left">Offer about task</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qw<sup>h</sup></td>
<td class="org-right">11</td>
<td class="org-left">qw</td>
<td class="org-left">Wh-Question, hold before answer</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">bc</td>
<td class="org-right">11</td>
<td class="org-left">bc</td>
<td class="org-left">Correct Misspeaking</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">+\*</td>
<td class="org-right">11</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">Continuation w/ transcription error</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">sd<sup>e</sup><sup>t</sup></td>
<td class="org-right">10</td>
<td class="org-left">sd</td>
<td class="org-left">Statement expanding y/n answer about task</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">na<sup>t</sup></td>
<td class="org-right">10</td>
<td class="org-left">na</td>
<td class="org-left">Affirmative Non-yes answer about task</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">qw@</td>
<td class="org-right">9</td>
<td class="org-left">qw</td>
<td class="org-left">Wh-question w/ error</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">fx</td>
<td class="org-right">9</td>
<td class="org-left">sv</td>
<td class="org-left">Explicit Performative</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sv,o@</td>
<td class="org-right">8</td>
<td class="org-left">sv</td>
<td class="org-left">Opinion, other w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sd<sup>e</sup>@</td>
<td class="org-right">8</td>
<td class="org-left">sd</td>
<td class="org-left">Statement expanding y/n answer w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">qy<sup>2</sup></td>
<td class="org-right">8</td>
<td class="org-left">qy</td>
<td class="org-left">Yes-no question w/ collaborative complete</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">bf@</td>
<td class="org-right">8</td>
<td class="org-left">bf</td>
<td class="org-left">Summarize/reformulate w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">ny<sup>m</sup></td>
<td class="org-right">7</td>
<td class="org-left">ny</td>
<td class="org-left">Yes Answer w/ Mimic</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">bd<sup>r</sup></td>
<td class="org-right">7</td>
<td class="org-left">bd</td>
<td class="org-left">Downplaying w/ repeat</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">b\*</td>
<td class="org-right">7</td>
<td class="org-left">b</td>
<td class="org-left">Continuer w/ transcription error</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">^2@</td>
<td class="org-right">7</td>
<td class="org-left">^2</td>
<td class="org-left">Collaborative Completion w/ error</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">qy<sup>d</sup><sup>r</sup></td>
<td class="org-right">6</td>
<td class="org-left">qy<sup>d</sup></td>
<td class="org-left">Declarative Yes-no Question w/ repeat</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qy<sup>d</sup>@</td>
<td class="org-right">6</td>
<td class="org-left">qy<sup>d</sup></td>
<td class="org-left">Declarative Yes-no Question w/ error</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qrr<sup>t</sup></td>
<td class="org-right">6</td>
<td class="org-left">qrr</td>
<td class="org-left">Or-question about task</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qo<sup>t</sup></td>
<td class="org-right">6</td>
<td class="org-left">qo</td>
<td class="org-left">Open Question about task</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">ny@</td>
<td class="org-right">6</td>
<td class="org-left">ny</td>
<td class="org-left">Yes Answer w/ transcription error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">nn<sup>m</sup></td>
<td class="org-right">6</td>
<td class="org-left">nn</td>
<td class="org-left">No answer w/ mimic</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">bh<sup>m</sup></td>
<td class="org-right">6</td>
<td class="org-left">bh</td>
<td class="org-left">Rhetorical Question w/ mimic</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">bf<sup>r</sup></td>
<td class="org-right">6</td>
<td class="org-left">bf</td>
<td class="org-left">Reformulate w/ repeat</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">ad(<sup>q</sup>)</td>
<td class="org-right">6</td>
<td class="org-left">ad</td>
<td class="org-left">Action direction w/ quotation</td>
<td class="org-left">Command</td>
</tr>


<tr>
<td class="org-left">^q<sup>t</sup></td>
<td class="org-right">6</td>
<td class="org-left">^q</td>
<td class="org-left">Quotation about task</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sv(<sup>q</sup>)@</td>
<td class="org-right">5</td>
<td class="org-left">sv</td>
<td class="org-left">Opinion w/ quotation and error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sd<sup>e</sup><sup>r</sup></td>
<td class="org-right">5</td>
<td class="org-left">sd</td>
<td class="org-left">Statement reply to y/n questions w/ repeat</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sd<sup>e</sup><sup>m</sup></td>
<td class="org-right">5</td>
<td class="org-left">sd</td>
<td class="org-left">Statement reply to y/n questions w/ mimic</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sd<sup>2</sup></td>
<td class="org-right">5</td>
<td class="org-left">sd</td>
<td class="org-left">Statement collaborative completion</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">qrr<sup>d</sup></td>
<td class="org-right">5</td>
<td class="org-left">qrr</td>
<td class="org-left">Declarative Or-question</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">o\*</td>
<td class="org-right">5</td>
<td class="org-left">bc</td>
<td class="org-left">Other w/ transcription error</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">nn<sup>e</sup></td>
<td class="org-right">5</td>
<td class="org-left">ng</td>
<td class="org-left">No answer to y/n question</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">fo</td>
<td class="org-right">5</td>
<td class="org-left">bc</td>
<td class="org-left">Other forward-function</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">^2<sup>g</sup></td>
<td class="org-right">5</td>
<td class="org-left">^2</td>
<td class="org-left">Collaborative completion, tag question</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">sd(<sup>q</sup>)@</td>
<td class="org-right">4</td>
<td class="org-left">sd</td>
<td class="org-left">Statement w/ quotation and error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sd(<sup>q</sup>)\*</td>
<td class="org-right">4</td>
<td class="org-left">sd</td>
<td class="org-left">Statement w/ quotation and trans. error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">qy<sup>g</sup>@</td>
<td class="org-right">4</td>
<td class="org-left">qy</td>
<td class="org-left">Yes-no tag question w/ error</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qy<sup>g</sup>\*</td>
<td class="org-right">4</td>
<td class="org-left">qy</td>
<td class="org-left">Yes-no tag question w/ transcription error</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qy<sup>d</sup><sup>m</sup></td>
<td class="org-right">4</td>
<td class="org-left">qy<sup>d</sup></td>
<td class="org-left">Declarative Yes-no question w/ mimic</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qy(<sup>q</sup>)</td>
<td class="org-right">4</td>
<td class="org-left">qy</td>
<td class="org-left">Yes-no Question w/ quotation</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qo<sup>d</sup></td>
<td class="org-right">4</td>
<td class="org-left">qo</td>
<td class="org-left">Declarative Open Question</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qh<sup>m</sup></td>
<td class="org-right">4</td>
<td class="org-left">qh</td>
<td class="org-left">Rhetorical Question w/ mimic</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">oo</td>
<td class="org-right">4</td>
<td class="org-left">cc</td>
<td class="org-left">Offer</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">o<sup>r</sup></td>
<td class="org-right">4</td>
<td class="org-left">bc</td>
<td class="org-left">Other w/ repeat</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">no<sup>t</sup></td>
<td class="org-right">4</td>
<td class="org-left">no</td>
<td class="org-left">Other answers about task</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">ng<sup>r</sup></td>
<td class="org-right">4</td>
<td class="org-left">ng</td>
<td class="org-left">Negative Non-no answer w/ repeat</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">h<sup>r</sup></td>
<td class="org-right">4</td>
<td class="org-left">h</td>
<td class="org-left">Hedge w/ repeat</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">ad<sup>r</sup></td>
<td class="org-right">4</td>
<td class="org-left">ad</td>
<td class="org-left">Action directive w/ repeat</td>
<td class="org-left">Command</td>
</tr>


<tr>
<td class="org-left">ad<sup>c</sup></td>
<td class="org-right">4</td>
<td class="org-left">ad</td>
<td class="org-left">Action directive about communication</td>
<td class="org-left">Command</td>
</tr>


<tr>
<td class="org-left">ad@</td>
<td class="org-right">4</td>
<td class="org-left">ad</td>
<td class="org-left">Action directive w/ error</td>
<td class="org-left">Command</td>
</tr>


<tr>
<td class="org-left">aa\*</td>
<td class="org-right">4</td>
<td class="org-left">aa</td>
<td class="org-left">Accept w/ transcription error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sv<sup>c</sup></td>
<td class="org-right">3</td>
<td class="org-left">sv</td>
<td class="org-left">Opinion about communication</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sv<sup>2</sup></td>
<td class="org-right">3</td>
<td class="org-left">sv</td>
<td class="org-left">Opinion w/ collaborative completion</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sv,sd,o@</td>
<td class="org-right">3</td>
<td class="org-left">sv</td>
<td class="org-left">Opinion, Statement, Other w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">qy\*</td>
<td class="org-right">3</td>
<td class="org-left">qy</td>
<td class="org-left">Yes-no Question w/ transcription error</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qw<sup>g</sup></td>
<td class="org-right">3</td>
<td class="org-left">qw</td>
<td class="org-left">Wh-Question tag question</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qw<sup>d</sup><sup>t</sup></td>
<td class="org-right">3</td>
<td class="org-left">qw<sup>d</sup></td>
<td class="org-left">Declarative Qh-Question about task</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qr<sup>t</sup></td>
<td class="org-right">3</td>
<td class="org-left">qy</td>
<td class="org-left">Or-question about task</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qh@</td>
<td class="org-right">3</td>
<td class="org-left">qh</td>
<td class="org-left">Rhetorical Question w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">o<sup>c</sup></td>
<td class="org-right">3</td>
<td class="org-left">bc</td>
<td class="org-left">Other about communication</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">nd<sup>t</sup></td>
<td class="org-right">3</td>
<td class="org-left">nd</td>
<td class="org-left">Dispreferred answer about task</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">na@</td>
<td class="org-right">3</td>
<td class="org-left">na</td>
<td class="org-left">Affirmative Yes-no Answer w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">fw</td>
<td class="org-right">3</td>
<td class="org-left">bc</td>
<td class="org-left">You're Welcome</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">fp<sup>r</sup></td>
<td class="org-right">3</td>
<td class="org-left">fp</td>
<td class="org-left">Conventional Opening w/ repeat</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">co<sup>c</sup></td>
<td class="org-right">3</td>
<td class="org-left">cc</td>
<td class="org-left">Offer about communication</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">bh<sup>r</sup></td>
<td class="org-right">3</td>
<td class="org-left">bh</td>
<td class="org-left">Backchannel in Question Form w/ repeat</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">bh@</td>
<td class="org-right">3</td>
<td class="org-left">bh</td>
<td class="org-left">Backchannel in Question Form w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">bf<sup>m</sup></td>
<td class="org-right">3</td>
<td class="org-left">bf</td>
<td class="org-left">Summarize w/ mimic</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">ba<sup>m</sup></td>
<td class="org-right">3</td>
<td class="org-left">ba</td>
<td class="org-left">Appreciation w/ mimic</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">b<sup>m</sup><sup>t</sup></td>
<td class="org-right">3</td>
<td class="org-left">b<sup>m</sup></td>
<td class="org-left">Repeat phrase about task</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">aa<sup>t</sup></td>
<td class="org-right">3</td>
<td class="org-left">aa</td>
<td class="org-left">Accept about task</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">aa<sup>2</sup></td>
<td class="org-right">3</td>
<td class="org-left">aa</td>
<td class="org-left">Accept w/ collaborative completion</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">^q@</td>
<td class="org-right">3</td>
<td class="org-left">^q</td>
<td class="org-left">Quotation w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">^q\*</td>
<td class="org-right">3</td>
<td class="org-left">^q</td>
<td class="org-left">Quotation w/ transcription error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">%\*</td>
<td class="org-right">3</td>
<td class="org-left">%</td>
<td class="org-left">Abandoned w/ transcription error</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">x\*</td>
<td class="org-right">2</td>
<td class="org-left">x</td>
<td class="org-left">Non-verbal w/ transcription error</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">sd<sup>q</sup></td>
<td class="org-right">2</td>
<td class="org-left">sd</td>
<td class="org-left">Statement w/ quotation</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">qy<sup>g</sup><sup>r</sup></td>
<td class="org-right">2</td>
<td class="org-left">qy</td>
<td class="org-left">Yes-no Tag Question w/ repeat</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qy<sup>g</sup><sup>c</sup></td>
<td class="org-right">2</td>
<td class="org-left">qy</td>
<td class="org-left">Yes-no Tag Question about communication</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qy<sup>d</sup><sup>h</sup></td>
<td class="org-right">2</td>
<td class="org-left">qy<sup>d</sup></td>
<td class="org-left">Declarative Yes-No Question hold</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qy<sup>c</sup><sup>r</sup></td>
<td class="org-right">2</td>
<td class="org-left">qy</td>
<td class="org-left">Yes-no about communication w/ repeat</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qw<sup>m</sup></td>
<td class="org-right">2</td>
<td class="org-left">qw</td>
<td class="org-left">Wh-question w/ mimic</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qw<sup>c</sup></td>
<td class="org-right">2</td>
<td class="org-left">qw</td>
<td class="org-left">Wh-question about communication</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qw\*</td>
<td class="org-right">2</td>
<td class="org-left">qw</td>
<td class="org-left">Wh-question w/ transcription error</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qh<sup>r</sup></td>
<td class="org-right">2</td>
<td class="org-left">qh</td>
<td class="org-left">Rhetorical Question w/ repeat</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">qh<sup>h</sup></td>
<td class="org-right">2</td>
<td class="org-left">qh</td>
<td class="org-left">Rhetorical Question w/ hold</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">oo<sup>t</sup></td>
<td class="org-right">2</td>
<td class="org-left">cc</td>
<td class="org-left">Open Offer about task</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">o<sup>t</sup></td>
<td class="org-right">2</td>
<td class="org-left">bc</td>
<td class="org-left">Other about task</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">ny<sup>e</sup></td>
<td class="org-right">2</td>
<td class="org-left">na</td>
<td class="org-left">Yes Answer Plus Expansion</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">ny<sup>c</sup></td>
<td class="org-right">2</td>
<td class="org-left">ny</td>
<td class="org-left">Yes Answer about communication</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">no<sup>r</sup></td>
<td class="org-right">2</td>
<td class="org-left">no</td>
<td class="org-left">Other Answer w/ repeat</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">nn\*</td>
<td class="org-right">2</td>
<td class="org-left">nn</td>
<td class="org-left">No Answer w/ transcription error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">ng<sup>m</sup></td>
<td class="org-right">2</td>
<td class="org-left">ng</td>
<td class="org-left">Negative Non-no Answer w/ mimic</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">h<sup>t</sup></td>
<td class="org-right">2</td>
<td class="org-left">h</td>
<td class="org-left">Hedge about task</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">fc@</td>
<td class="org-right">2</td>
<td class="org-left">fc</td>
<td class="org-left">Conventional closing w/ error</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">fa<sup>c</sup></td>
<td class="org-right">2</td>
<td class="org-left">fa</td>
<td class="org-left">Apology about communication</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">cc<sup>r</sup></td>
<td class="org-right">2</td>
<td class="org-left">cc</td>
<td class="org-left">Commit w/ repeat</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">br<sup>r</sup></td>
<td class="org-right">2</td>
<td class="org-left">br</td>
<td class="org-left">Signal Non-Understanding w/ repeat</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">bk@</td>
<td class="org-right">2</td>
<td class="org-left">bk</td>
<td class="org-left">Acknowledge w/ error</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">bf<sup>t</sup></td>
<td class="org-right">2</td>
<td class="org-left">bf</td>
<td class="org-left">Reformulation about task</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">bf<sup>g</sup></td>
<td class="org-right">2</td>
<td class="org-left">bf</td>
<td class="org-left">Reformulation Tag Question</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">bf\*</td>
<td class="org-right">2</td>
<td class="org-left">bf</td>
<td class="org-left">Reformulation w/ transcription error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">bf(<sup>q</sup>)</td>
<td class="org-right">2</td>
<td class="org-left">bf</td>
<td class="org-left">Reformulation w/ quotation</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">bc<sup>r</sup></td>
<td class="org-right">2</td>
<td class="org-left">bc</td>
<td class="org-left">Correct Misspeaking w/ repeat</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">b<sup>m</sup><sup>r</sup></td>
<td class="org-right">2</td>
<td class="org-left">b<sup>m</sup></td>
<td class="org-left">Continuer w/ mimic and repeat</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">b<sup>m</sup><sup>g</sup></td>
<td class="org-right">2</td>
<td class="org-left">b<sup>m</sup></td>
<td class="org-left">Tag Question Continuer w/ mimic</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">b<sup>m</sup>@</td>
<td class="org-right">2</td>
<td class="org-left">b<sup>m</sup></td>
<td class="org-left">Continuer w/ mimic and error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">am<sup>r</sup></td>
<td class="org-right">2</td>
<td class="org-left">am</td>
<td class="org-left">Maybe w/ repeat</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">ad\*</td>
<td class="org-right">2</td>
<td class="org-left">ad</td>
<td class="org-left">Action directive w/ error</td>
<td class="org-left">Command</td>
</tr>


<tr>
<td class="org-left">aa,o@</td>
<td class="org-right">2</td>
<td class="org-left">aa</td>
<td class="org-left">Accept, Other w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">^q<sup>r</sup></td>
<td class="org-right">2</td>
<td class="org-left">^q</td>
<td class="org-left">Quotation Repeat</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">^h<sup>r</sup></td>
<td class="org-right">2</td>
<td class="org-left">^h</td>
<td class="org-left">Hold w/ repeat</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">^2\*</td>
<td class="org-right">2</td>
<td class="org-left">^2</td>
<td class="org-left">Collaborative Completion w/ transcript error</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">t1<sup>t</sup></td>
<td class="org-right">1</td>
<td class="org-left">t1</td>
<td class="org-left">Self-talk about task</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">sv<sup>e</sup><sup>r</sup></td>
<td class="org-right">1</td>
<td class="org-left">sv</td>
<td class="org-left">Opinion Answer w/ repeat</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sv;sd</td>
<td class="org-right">1</td>
<td class="org-left">sv</td>
<td class="org-left">Opinion, statement</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sv,qy<sup>g</sup>@</td>
<td class="org-right">1</td>
<td class="org-left">sv</td>
<td class="org-left">Opinion, Yes-no Tag Question</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sv(<sup>q</sup>)\*</td>
<td class="org-right">1</td>
<td class="org-left">sv</td>
<td class="org-left">Opinion w/ Quotation and Error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sd<sup>t</sup>\*</td>
<td class="org-right">1</td>
<td class="org-left">sd</td>
<td class="org-left">Statement about task w/ transcription error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sd<sup>r</sup>@</td>
<td class="org-right">1</td>
<td class="org-left">sd</td>
<td class="org-left">Statement w/ repeat and error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sd<sup>m</sup>@</td>
<td class="org-right">1</td>
<td class="org-left">sd</td>
<td class="org-left">Statement w/ mimic and error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sd<sup>m</sup>\*</td>
<td class="org-right">1</td>
<td class="org-left">sd</td>
<td class="org-left">Statement w/ mimic and transcription error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sd<sup>e</sup>(<sup>q</sup>)<sup>r</sup></td>
<td class="org-right">1</td>
<td class="org-left">sd</td>
<td class="org-left">Statement exp of y/n quest. w/ quote/repeat</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sd;sv</td>
<td class="org-right">1</td>
<td class="org-left">sv</td>
<td class="org-left">Statement, opinion</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sd;qy<sup>d</sup></td>
<td class="org-right">1</td>
<td class="org-left">sd</td>
<td class="org-left">Statement, Declarative Yes-no Question</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sd;no</td>
<td class="org-right">1</td>
<td class="org-left">sd</td>
<td class="org-left">Statement, Other Answer</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sd,sv</td>
<td class="org-right">1</td>
<td class="org-left">sv</td>
<td class="org-left">Statement, Opinion</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sd,qy<sup>g</sup></td>
<td class="org-right">1</td>
<td class="org-left">sd</td>
<td class="org-left">Statement, Yes-no Tag Question</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">sd(<sup>q</sup>)<sup>r</sup></td>
<td class="org-right">1</td>
<td class="org-left">sd</td>
<td class="org-left">Statement w/ Quotation and repeat</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">qy<sup>h</sup>@</td>
<td class="org-right">1</td>
<td class="org-left">qy</td>
<td class="org-left">Yes-no Question, hold w/ error</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qy<sup>d</sup><sup>c</sup></td>
<td class="org-right">1</td>
<td class="org-left">qy<sup>d</sup></td>
<td class="org-left">Declarative Yes-no Question about comm</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qy<sup>d</sup>\*</td>
<td class="org-right">1</td>
<td class="org-left">qy<sup>d</sup></td>
<td class="org-left">Declarative Yes-no Question w/ transc. error</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qy<sup>d</sup>(<sup>q</sup>)</td>
<td class="org-right">1</td>
<td class="org-left">qy<sup>d</sup></td>
<td class="org-left">Declarative Yes-no Question w/ quotation</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qy,am,o@</td>
<td class="org-right">1</td>
<td class="org-left">qy</td>
<td class="org-left">Yes-no Question, Maybe, Other w/ error</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qw<sup>t</sup>@</td>
<td class="org-right">1</td>
<td class="org-left">qw</td>
<td class="org-left">Wh-question about task w/ error</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qw<sup>r</sup><sup>t</sup></td>
<td class="org-right">1</td>
<td class="org-left">qw</td>
<td class="org-left">Wh-Question w/ repeat about task</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qw<sup>d</sup><sup>m</sup></td>
<td class="org-right">1</td>
<td class="org-left">qw<sup>d</sup></td>
<td class="org-left">Declarative Wh-Question w/ mimic</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qw<sup>d</sup><sup>c</sup></td>
<td class="org-right">1</td>
<td class="org-left">qw<sup>d</sup></td>
<td class="org-left">Declarative Wh-Question about communication</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qw<sup>d</sup>@</td>
<td class="org-right">1</td>
<td class="org-left">qw<sup>d</sup></td>
<td class="org-left">Declarative Wh-Question w/ error</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qw(<sup>q</sup>)</td>
<td class="org-right">1</td>
<td class="org-left">qw</td>
<td class="org-left">Wh-Question w/ quotation</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qrr@</td>
<td class="org-right">1</td>
<td class="org-left">qrr</td>
<td class="org-left">Or-question w/ error</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qr<sup>d</sup>\*</td>
<td class="org-right">1</td>
<td class="org-left">qy</td>
<td class="org-left">Declarative Or question w/ trans. error</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qr(<sup>q</sup>)</td>
<td class="org-right">1</td>
<td class="org-left">qy</td>
<td class="org-left">Or-question w/ quotation</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qo<sup>r</sup></td>
<td class="org-right">1</td>
<td class="org-left">qo</td>
<td class="org-left">Open-ended question w/ repeat</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qo<sup>d</sup><sup>c</sup></td>
<td class="org-right">1</td>
<td class="org-left">qo</td>
<td class="org-left">Decl Open-ended question about comm</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qo@</td>
<td class="org-right">1</td>
<td class="org-left">qo</td>
<td class="org-left">Open Ended Question w/ error</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">qh<sup>g</sup></td>
<td class="org-right">1</td>
<td class="org-left">qh</td>
<td class="org-left">Rhetorical Tag Question</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">qh<sup>c</sup></td>
<td class="org-right">1</td>
<td class="org-left">qh</td>
<td class="org-left">Rhetorical Question about communication</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">qh\*</td>
<td class="org-right">1</td>
<td class="org-left">qh</td>
<td class="org-left">Rhetorical Question with transcription error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">qh(<sup>q</sup>)</td>
<td class="org-right">1</td>
<td class="org-left">qh</td>
<td class="org-left">Rhetorical Question with quotation</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">oo(<sup>q</sup>)</td>
<td class="org-right">1</td>
<td class="org-left">cc</td>
<td class="org-left">Offer with Quotation</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">ny<sup>t</sup></td>
<td class="org-right">1</td>
<td class="org-left">ny</td>
<td class="org-left">Yes Answer about task</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">ny<sup>c</sup><sup>r</sup></td>
<td class="org-right">1</td>
<td class="org-left">ny</td>
<td class="org-left">Yes Answer about communication w/ repeat</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">ny\*</td>
<td class="org-right">1</td>
<td class="org-left">ny</td>
<td class="org-left">Yes Answer w/ transcription error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">no@</td>
<td class="org-right">1</td>
<td class="org-left">no</td>
<td class="org-left">Other answer w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">nn<sup>t</sup></td>
<td class="org-right">1</td>
<td class="org-left">nn</td>
<td class="org-left">No Answers about task</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">nn<sup>r</sup><sup>t</sup></td>
<td class="org-right">1</td>
<td class="org-left">nn</td>
<td class="org-left">No Answers w/ repeat about task</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">nn<sup>r</sup>@</td>
<td class="org-right">1</td>
<td class="org-left">nn</td>
<td class="org-left">No Answers w/ repeat and error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">ng<sup>t</sup></td>
<td class="org-right">1</td>
<td class="org-left">ng</td>
<td class="org-left">Negative Non-no Answers about task</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">ng<sup>r,o</sup>@</td>
<td class="org-right">1</td>
<td class="org-left">ng</td>
<td class="org-left">Neg Non-No Answers w/ repeat, other w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">na<sup>m</sup><sup>t</sup></td>
<td class="org-right">1</td>
<td class="org-left">na</td>
<td class="org-left">Aff Non-Yes Answers w/ mimic about task</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">na,sd,o@</td>
<td class="org-right">1</td>
<td class="org-left">na</td>
<td class="org-left">Affirmative Non-Yes Answer, Statement, Other</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">h<sup>m</sup></td>
<td class="org-right">1</td>
<td class="org-left">h</td>
<td class="org-left">Hold w/ mimic</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">h@</td>
<td class="org-right">1</td>
<td class="org-left">h</td>
<td class="org-left">Hold w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">h,sd</td>
<td class="org-right">1</td>
<td class="org-left">h</td>
<td class="org-left">Hold, statement</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">fw\*</td>
<td class="org-right">1</td>
<td class="org-left">bc</td>
<td class="org-left">You're Welcome w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">ft<sup>t</sup></td>
<td class="org-right">1</td>
<td class="org-left">ft</td>
<td class="org-left">Thanking about task</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">ft<sup>m</sup></td>
<td class="org-right">1</td>
<td class="org-left">ft</td>
<td class="org-left">Thanking w/ mimic</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">fo<sup>c</sup></td>
<td class="org-right">1</td>
<td class="org-left">bc</td>
<td class="org-left">Other forward function about communication</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">fc,o@</td>
<td class="org-right">1</td>
<td class="org-left">fc</td>
<td class="org-left">Conventional Closing, Other w/ error</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">fa<sup>t</sup></td>
<td class="org-right">1</td>
<td class="org-left">fa</td>
<td class="org-left">Apology about task</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">fa<sup>r</sup></td>
<td class="org-right">1</td>
<td class="org-left">fa</td>
<td class="org-left">Apology w/ repeat</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">cc<sup>t</sup></td>
<td class="org-right">1</td>
<td class="org-left">cc</td>
<td class="org-left">Commit about task</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">br,o@</td>
<td class="org-right">1</td>
<td class="org-left">br</td>
<td class="org-left">Signal Non-Understanding, Other w/ error</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">bk<sup>t</sup></td>
<td class="org-right">1</td>
<td class="org-left">bk</td>
<td class="org-left">Response Acknowledgement about task</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">bk,sd,o@</td>
<td class="org-right">1</td>
<td class="org-left">bk</td>
<td class="org-left">Acknowledgement, Statement, Other w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">bh,sd,o@</td>
<td class="org-right">1</td>
<td class="org-left">bh</td>
<td class="org-left">Backchannel, Statement, Other w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">bf<sup>2</sup></td>
<td class="org-right">1</td>
<td class="org-left">bf</td>
<td class="org-left">Reformulation w/ collaborative completion</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">bf,nn,o@</td>
<td class="org-right">1</td>
<td class="org-left">bf</td>
<td class="org-left">Reformulation, No Answer, Other w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">bd@</td>
<td class="org-right">1</td>
<td class="org-left">bd</td>
<td class="org-left">Downplayer w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">ba<sup>m</sup>@</td>
<td class="org-right">1</td>
<td class="org-left">ba</td>
<td class="org-left">Appreciation w/ mimic and error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">ba,fe</td>
<td class="org-right">1</td>
<td class="org-left">ba</td>
<td class="org-left">Appreciation, Exclamation</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">b<sup>t</sup></td>
<td class="org-right">1</td>
<td class="org-left">b</td>
<td class="org-left">Continuer about task</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">b<sup>r</sup>@</td>
<td class="org-right">1</td>
<td class="org-left">b</td>
<td class="org-left">Continuer w/ repeat and error</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">b<sup>m,sd,o</sup>@</td>
<td class="org-right">1</td>
<td class="org-left">b<sup>m</sup></td>
<td class="org-left">Cont. w/ mimic, statement, other w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">b<sup>2</sup></td>
<td class="org-right">1</td>
<td class="org-left">b</td>
<td class="org-left">Continuer w/ collaborative completion</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">ar<sup>m</sup></td>
<td class="org-right">1</td>
<td class="org-left">ar</td>
<td class="org-left">Reject w/ mimic</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">ad,qy@</td>
<td class="org-right">1</td>
<td class="org-left">ad</td>
<td class="org-left">Action directive, Yes-no Question w/ error</td>
<td class="org-left">Command</td>
</tr>


<tr>
<td class="org-left">ad,o@</td>
<td class="org-right">1</td>
<td class="org-left">ad</td>
<td class="org-left">Action directive, Other w/ error</td>
<td class="org-left">Command</td>
</tr>


<tr>
<td class="org-left">aap<sup>r</sup></td>
<td class="org-right">1</td>
<td class="org-left">am</td>
<td class="org-left">Accept Part w/ repeat</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">aap<sup>m</sup></td>
<td class="org-right">1</td>
<td class="org-left">am</td>
<td class="org-left">Accept Part w/ mimic</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">aa<sup>r,o</sup>@</td>
<td class="org-right">1</td>
<td class="org-left">aa</td>
<td class="org-left">Accept w/ repeat, other w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">aa<sup>h</sup></td>
<td class="org-right">1</td>
<td class="org-left">aa</td>
<td class="org-left">Accept & hold</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">aa,ar</td>
<td class="org-right">1</td>
<td class="org-left">aa</td>
<td class="org-left">Accept, Reject</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">^h<sup>t</sup></td>
<td class="org-right">1</td>
<td class="org-left">^h</td>
<td class="org-left">Hold about task</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">^h@</td>
<td class="org-right">1</td>
<td class="org-left">^h</td>
<td class="org-left">Hold w/ error</td>
<td class="org-left">Statement</td>
</tr>


<tr>
<td class="org-left">^g@</td>
<td class="org-right">1</td>
<td class="org-left">^g</td>
<td class="org-left">Tag Question w/ error</td>
<td class="org-left">Question</td>
</tr>


<tr>
<td class="org-left">^2<sup>t</sup></td>
<td class="org-right">1</td>
<td class="org-left">^2</td>
<td class="org-left">Collaborative completion about task</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">^2<sup>r</sup></td>
<td class="org-right">1</td>
<td class="org-left">^2</td>
<td class="org-left">Collaborative completion w/ repeat</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">%@\*</td>
<td class="org-right">1</td>
<td class="org-left">%</td>
<td class="org-left">Abandoned w/ errors</td>
<td class="org-left">Other</td>
</tr>


<tr>
<td class="org-left">%,o@</td>
<td class="org-right">1</td>
<td class="org-left">%</td>
<td class="org-left">Abandoned, other w/ error</td>
<td class="org-left">Other</td>
</tr>
</tbody>
</table>

