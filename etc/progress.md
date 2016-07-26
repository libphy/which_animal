### 7/15/2016

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

### 7/16/2016  
Got the mfcc and deltas to work. I found and tested a few audio signal processing tools online, and ended up using librosa package which also calculates deltas unlike other packages.  
It also has a visualization tool, and I tested cat meows and dog barking sounds.  
Exploratory analysis is done in in Test.ipynb  

### 7/17/2016  
Understood how librosa mfcc/delta calculation algorithm and what parameters values are used in the algorithm.  
Checked validity of those parameter values.  
- sr: 22050 sampling rate  
- n_fft: 2048 number of samples in a fft window (~10 ms long frame). In speech recognition 10 ms- 40 ms frame window have been used.  
- hop_length: step size when doing STFT (2.5 ms sliding)    
- n_mfcc : 20 number of mel frequency cepstral coefficients. Normally 20-40 is used in speech recognition. 7 coefficients known to be ok with animal sounds.  

Data duration and number of data.  
Slicing the sound data to 1 second duration would be sufficient since most of meows and barks is shorter than 1 s (exceptions exist depending on the animal's vocalization)  
1 s duration yields 44 frames thus final mfcc array for 20 mfcc looks like 20x44.  
Slicing to a few seconds may be fine as well. Also detecting when a meow/bark is and slicing such that there is one or more meow/bark in a fixed duration would be beneficial to create more than one data point in a sound file.    
Compared to bird chirp sounds, domestic animal sounds are very rare in data repositories since birds sounds are of more importance in biology research. So slicing to multiple data points will be beneficial.    

To do:  
- write a script that detects peaks and slices sound data around that peak
modify scraping german site such that it scrapes tags (meow, purr, hiss, etc)
- Scrape more data -> freesound.org

peak detection function done

### 7/18/2016  
scraping script for freesound.org using selenium.
inspected cat meow sounds, created block words list.
wrote a script that scrape only relevant download links (filters out cat sounds other than meow, noise and irrelevant tags).

### 7/19/2016  
- inspected further sound data and tweaked filters.
- downloaded cat meow files (resulted in 69 selected files list out of 398 listings).
- wrote a script that renames the audio files and converts from arbitrary audio file format to .wav format.

To do:  
- inspect sound files- duration, sampling rate etc
- modify scraping script for german animal sound repo (tierstimmen) to filter certain tags -> get cat meow filtered files -> consolidate all cat meows
- write a script that slices a long sound files to multiple ones (using peak detection) and makes a short one padded  

- scrape dog barking sound data from freesound.org, need to create block words for dog sound

### 7/20/2016  
- worked hard on inspecting cat sound and create a dataframe: cat_inspect_df.ipynb
  - -> df pickled : cat_inspect_df.pkl
- cleaned them and wrote a code to detect signals: cat_slice_test.ipynb
  - -> df pickled : cat_slice_df.pkl
- sound that contains meow from ts and fs is about 300 s long total, and 0.6 s is for one meow.
- I ended up downloading 6 hour long video from youtube.
Then converted to audio using www.mp3fy.com  
It was 350 MB m4a file, then it became 3.8 GB when converted to wav.  
I discovered that 6 hour meow file is actually repeated 4 min, so I decided not to use it.
- Finalized selecting cat sound files to use and saved their tagging info in the data frame.
- Updated saved pickles.

### 7/21/2106  
- Worked on dog annotation file scraper.
- Inspect dog sound files and annotation files.
- Selected dog sound files and saved tagging info in the pandas dataframe, then saved as pickle.

### 7/22/2016-7/23/2016  
I was sick, so I had a little progress.
- Worked on git house keeping.
  - Got rid of huge binary files from remote and local repo.
  - Got rid of .git objects that has large size. (see os_notes/git_notes repo for how to)
  - Permanently erased git commit histories for files that has sensitive data.
  - Modified files with sensitive data to use os.environ() instead.
  - Updated .gitignore
  - Manually version controlled and synced three repos (local mac, local linux, remote)
- Cleaned up and organized folders and files in local machine.

### 7/24/2016  
- Wrote a code that makes time series segments from audio files then calculates mfcc and deltas from time series segments
- Configured and tested mfcc's arguments.
- Calculation of mfcc has been done using 25 ms fft window 10 ms slide, 1 second duration of segments
- Currently, segments slicing has no overlaps when the dataframe active region tuple duration is longer than segment duration.
However, in case the tuples are close to each other it does not take it into account thus there may be overlaps (this is more prune to spiky regions in the audio file).

### 7/25/2016  
- Wrote a code that concatenates mfcc/delta/delta2 arrays and trims to make a square shaped image patches. When calculating mfcc, I used 13 mfcc coefficients for 1 s duration data, 50 ms fft window width and 25 ms slides to make 13x41 arrays for each of mfcc, delta and delta2. The concatenated array demension is 13*3 by 41 = 39 by 41, then I trimmed the first and last columns such that the image patch array shape is 39 by 39.
- Tried using simple 1d NN with tensorflow but it didn't work-> decided to switch back to keras.
- Reinstalled and configured correctly to fix problems on making keras with tensorflow backend to work, and made it gpu-enabled.
- Worked on single layer 2d convolution net.  
  - At first it didn't work and gave all zeros or all ones.
I noticed a mistake that I didn't rescale the arrays so it had large negative and positive values.
So I rescaled them such that minimum of the concatenated array is 0 and maximum is 1, however the output of simple model was still all zero.  
I noticed that the original mfcc arrays have huge negative values in the first raw (lowest mel frequency band), distinguished from all other rows, which may still push other rows to white side in the image. And it seems to appear in all files regardless of sounds types.  
  - So I modified codes to filter the first row out and produce 36x36 rescaled image patches.  
Then it worked for the simple one-layer 2d conv net and it gave about 80% accuracy and 80% precision for binary (dog & cat) classification when 3000 data are used.  
  - I tested two rescaling methods: (1) rescaling each mfcc/delta/delta2 matrix by its own max absolute amplitude. (2) rescaling mfcc/delta/delta2 all at once by global max of amplitude. I ran 1 layer 2dconv but there was no difference in performance to both cases: 80% precision and 80% accuracy.  

  - The simple one layer 2d conv model uses mostly default hyper parameter values.
    - nb_filter =64, kernel size 3x3 for 2d conv layer
    - lr=0.001, decay=0.01, momentum=0.9 for SGD -> later tweaked to lr around 0.005 which brings performance from below 80% to over 80%.
    - For training, train, test split ratio was 8:2, shuffled.
    - default n_batch =32, n_epoch =10 for training.
    Playing with those two gave 4-5% better result. Best observed when n_batch was 1 with n_epoch =100 (could be shorter).  

- Got result like below

|  class | precision | recall   | f1-score  |support |
| ------|:---------:| :--------:|:---------:|-------:|
| 0.0   |  0.91     |   0.85    |  0.88     |   406 |
| 1.0   |    0.72   |   0.81    |  0.77     |   193 |
| avg / total   |    0.85 |     0.84 |     0.84 |    599 |
