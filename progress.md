7/15/2016

I found randomly in internet a resource where mfcc is calculated using scikits.audiolab andsscikits.talkbox, so decided to try them.
Installed scikits.audiolab and libsndfile : https://pypi.python.org/pypi/scikits.audiolab/
Installed scikits.talkbox

Since audiolab doesn't support mp3 for license issue, I had to convert mp3 files to other format.  .ogg is as compact as mp3.
Installed ffmpeg to convert mp3- the easiest way to install in mac is brew install ffmpeg, may need to install [yasm](http://macappstore.org/yasm/)) as well.

Tested conversion and it works. I found that I need to rename file names in order to make batch conversion easier. [ffmpeg file conversion](https://ffmpeg.org/ffmpeg.html#Video-and-Audio-file-format-conversion)
Unfortunately, audiolab's file read didn't work for ogg as it's supposed to, so I converted mp3 to wav.

The sound file is about 9s long and the sample rate is 44.1kHz (sounds like an overkill). Played with tools in thinkdsp package, visualized a spectrogram. Spectrogram (intensity vs time) doesn't distinguish a lot between cats and dogs other than dog's barking sound has a sharper shape of the signal envelop.
Fed sound signal into scikits' mfcc function. mel-frequency cepstral coefficients are 13 by default. I'm not sure how it slices fft windows, but it gives an extremely elongated shape of array. The resulting np array includes nans and infs at the very first and last <40 frames.
It wasn't so convenient to visualize them for its shape and values. Also comparing with thinkdsp package, every different packages seems to use its own normalization method for intensity as well.
So I decided to look for another package which has a consistency and use parameter values that are common in speech recognition when calculating stuff.

7/16/2016
Got the mfcc and deltas to work. I found and tested a few audio signal processing tools online, and ended up using librosa package which also calculates deltas unlike other packages.
It also has a visualization tool, and I tested cat meows and dog barking sounds.
Exploratory analysis is done in in Test.ipynb  

7/17/2016
Understood how librosa mfcc/delta calculation algorithm and what parameters values are used in the algorithm.
Checked validity of those parameter values.
sr: 22050 sampling rate
n_fft: 2048 number of samples in a fft window (~10 ms long frame). In speech recognition 10 ms- 40 ms frame window have been used.
hop_length: step size when doing STFT (2.5 ms hanning window)  
n_mfcc : 20 number of mel frequency cepstral coefficients. Normally 20-40 is used in speech recognition. 7 coefficients known to be ok with animal sounds.

Data duration and number of data.
Slicing the sound data to 1 second duration would be sufficient since most of meows and barks is shorter than 1 s (exceptions exist depending on the animal's vocalization)
1 s duration yields 44 frames thus final mfcc array for 20 mfcc looks like 20x44.
Slicing to a few seconds may be fine as well. Also detecting when a meow/bark is and slicing such that there is one or more meow/bark in a fixed duration would be beneficial to create more than one data point in a sound file.  
Compared to bird chirp sounds, domestic animal sounds are very rare in data repositories since birds sounds are of more importance in biology research. So slicing to multiple data points will be beneficial.  

To do:
write a script that detects peaks and slices sound data around that peak
modify scraping german site such that it scrapes tags (meow, purr, hiss, etc)
Scrape more data -> freesound.org
