7/15/2016

Installed scikits.audiolab and libsndfile : https://pypi.python.org/pypi/scikits.audiolab/

Since audiolab doesn't support mp3 for license issue, I had to convert mp3 files to other format. It seems that .ogg is as compact as mp3.
Installed ffmpeg to convert mp3 to ogg
(easiest way to install in mac is brew install ffmpeg, may need to install yasm as well: follow instruction on http://macappstore.org/yasm/)

Tested conversion and it works. I found that I need to rename file names in order to make batch conversion easier.
examples:  https://ffmpeg.org/ffmpeg.html#Video-and-Audio-file-format-conversion
Unfortunately, audiolab's file read didn't work for ogg.

Finally, I read the file in python and got mfcc, which gives numpy array. The sound file is about 9s long and the sample rate was by default 44.1kHz (sounds too mych) and mel-frequency cepstral coefficients are 13 by default, so it gives an elongated shape of array. The file include nan and infs at the very first and last <40 frames so I chopped them.
However plotting them showed all black squares. Maybe numbers are out of range of plotting tool.

Hmm.. another tool? (even has regression tools)
http://journals.plos.org/plosone/article/asset?id=10.1371/journal.pone.0144610.PDF
