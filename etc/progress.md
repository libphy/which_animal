### 7/15/2016

I found randomly in internet a resource where mfcc is calculated using scikits.audiolab andsscikits.talkbox, so decided to try them.
Installed scikits.audiolab and libsndfile : https://pypi.python.org/pypi/scikits.audiolab/
Installed scikits.talkbox  
(** I ended up not using these tools.)

Since audiolab doesn't support mp3 for license issue, I had to convert mp3 files to other format.  .ogg is as compact as mp3.
Installed ffmpeg to convert mp3- the easiest way to install in mac is brew install ffmpeg, may need to install [yasm](http://macappstore.org/yasm/) as well.

Tested conversion and it works. I found that I need to rename file names in order to make batch conversion easier. [ffmpeg file conversion](https://ffmpeg.org/ffmpeg.html#Video-and-Audio-file-format-conversion)
Unfortunately, audiolab's file read didn't work for ogg as it's supposed to, so I converted mp3 to wav.

The sound file is about 9s long and the sample rate is 44.1kHz (sounds like an overkill). Played with tools in thinkdsp package, visualized a spectrogram. Spectrogram (intensity vs time) doesn't distinguish a lot between cats and dogs other than dog's barking sound has a sharper shape of the signal envelop.
Fed sound signal into scikits' mfcc function. mel-frequency cepstral coefficients are 13 by default. I'm not sure how it slices fft windows, but it gives an extremely elongated shape of array. The resulting np array includes nans and infs at the very first and last <40 frames.
It wasn't so convenient to visualize them for its shape and values. Also comparing with thinkdsp package, every different packages seems to use its own normalization method for intensity as well.
So I decided to look for another package which has a consistency and use parameter values that are common in speech recognition when calculating stuff.

### 7/16/2016  
Got the mfcc and deltas to work. I found and tested a few audio signal processing tools online, and ended up using [librosa package](https://github.com/librosa/librosa) which also calculates deltas unlike other packages.  
It also has a visualization tool, and I tested cat meows and dog barking sounds.  
Exploratory analysis is done in Test.ipynb  

### 7/17/2016  
Understood how librosa mfcc/delta calculation algorithm and what parameters values are used in the algorithm.  
Checked validity of those parameter values.  
- sr: 22050 sampling rate  
- n_fft: 2048 number of samples in a fft window (<100 ms long at 22050 sr). In speech recognition 10 ms- 40 ms frame window have been used.  
- hop_length: step size when doing STFT ( default 512 frames meaning <25 ms sliding at 22050 sr)    
- n_mfcc : 20 number of mel frequency cepstral coefficients. Normally 13-20 is used in speech recognition (also 40 were used in some research). 7 coefficients known to be ok with some animal sounds.  

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
- I ended up downloading 6 hour long video that has cat sounds from youtube.
Then converted to audio using www.mp3fy.com  
It was 350 MB m4a file, then it became 3.8 GB when converted to wav format.  
Later I discovered that 6 hour meow file is actually repeated 4 min, so I decided not to use it.
- Finalized selecting cat sound files to use and saved their tagging info in the data frame.
- Updated saved pickles.

### 7/21/2106  
- Worked on dog annotation file scraper.
- Inspect dog sound files and annotation files.
- Selected dog sound files and saved tagging info in the pandas dataframe, then saved as pickle.

### 7/22/2016-7/23/2016  
I was sick, so I had little progress.
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
- Wrote a code that concatenates mfcc/delta/delta2 arrays and trims to make a square shaped image patches. When calculating mfcc, to reduce the image/array size further, I used 13 mfcc coefficients for 1 s duration data, 50 ms fft window width and 25 ms slides to make 13x41 arrays for each of mfcc, delta and delta2. The concatenated array patch demension is 13*3 by 41 = 39 by 41, then I trimmed the first and last columns such that the image patch array shape is 39 by 39.
- Tried using simple 1d NN with tensorflow but it didn't work-> decided to switch back to keras.
- Reinstalled and configured correctly to fix problems on making keras with tensorflow backend to work, and made it gpu-enabled.
- Worked on single layer 2d convolution net.  
  - At first it didn't work and gave all zeros or all ones.
I noticed a mistake that I didn't rescale the arrays so it had large negative and positive values.
So I rescaled them such that minimum of the concatenated array (39x39) is 0 and maximum is 1, however the output of simple model was still all zero.  
I noticed that the original mfcc arrays have huge negative values in the first row (lowest mel frequency band), distinguished from all other rows, which may still push other rows to white side in the image. And it seems to appear in all files regardless of sounds types.  
  - So I modified codes to filter the first row out and produce 36x36 rescaled image patches.  
Then it worked for the simple one-layer 2d conv net and it gave about 80% accuracy and 80% precision for binary (dog & cat) classification when 3000 data are used.  
  - I tested two rescaling methods: (1) rescaling each mfcc/delta/delta2 matrix by its own max absolute amplitude. (2) rescaling the concatenated patch (mfcc+delta+delta2) all at once by global max amplitude in the patch. I ran 1 layer 2dconv but there was no difference in performance to both cases (80% precision and 80% accuracy) although rescaling each seemed to have more features (wrinkles in the array image) noticeable by human eyes.  

  - The simple one-layer 2d conv model used mostly default hyper parameter values, but performing slightly better when some were tweaked.
    - nb_filter =64, kernel size 3x3 for 2d conv layer
    - lr=0.001, decay=0.01, momentum=0.9 for SGD -> later tweaked learning rate (lr) to around 0.005 which brings performance from below 80% to over 80%.
    - For training, train-test split ratio was 8:2, shuffled.
    - default n_batch =32, n_epoch =10 for training.
    Playing with those two gave 4-5% better result. Best observed when n_batch = 1 and n_epoch =100 (n_epoch could be shorter).  

- Got result like below

|  class | precision | recall   | f1-score  |support |
| ------|:---------:| :--------:|:---------:|-------:|
| 0.0   |  0.91     |   0.85    |  0.88     |   406 |
| 1.0   |    0.72   |   0.81    |  0.77     |   193 |
| avg / total   |    0.85 |     0.84 |     0.84 |    599 |

### 7/26/2016
I split training set further to have validation set within the training.
training:validation = 8:2.
I tested an idea about convolution kernel shape in single-layer conv model.
Since the mfcc array's vertical axis is mel frequency features and horizontal axis is a quantized time domain, I thought applying a convolution to only vertical axis or only horizontal axis may have some different result. I've tested several (nb_row x nb_col) shape filters and compared results for (3x1), (1x3), (1x5), (3x3) set and (3x3), (5x3) set, and confirmed that increasing/decreasing nb_row didn't affect (taking convolution in time axis) but increasing convolution size (nb_col) in frequency feature axis from 3 to 5 made it worse. Deceasing nb_col from 3 to 1 didn't change result.
Overall, the best performance was unchanged: 84-85%

I moved on to multi-layer 2dCNN models. Since the degree of freedom for the architectures and the hyper-parameters are quite big, I decided to get some heuristics on choosing architectures. After discussions and reading online resources about deep cnn architectures, I've got some ideas and tested/implemented some of them.

- Initialization of Conv layers:  
 Keras takes care of initialization for 2D convolution layer by default 'init'=glorot_uniform. I found whole a lot of opinions on which initialization methods should one use. But since my model doesn't fail in my test 2-conv-layer model, I decided to leave it as it is.

- Regularization in conv layers: I have not explored, but I think it's also important.  

- Zero-padding in Conv layers:
One convolution in one conv layer shrinks each dimension size by 2 pixels when 3x3 kernel is used or shrinks much faster if bigger size kernel is used. When having multiple conv layers quickly shrinks the array size and leaves less information for later layers. Zero padding in each conv layer has been a common practice in recent deep neural nets. I checked if Keras's 2d conv layer has zeropadding included by pulling out an output array from a conv layer and there was no zero padding built in 'Convolution2D'. But instead, Kearas has a separate layer 'ZeroPadding2D' that can be added before the  'Convolution2D'.

- Pooling layers:   
Helps the net see the bigger field of view. It's also like down-sampling, so the net can see overall shapes rather than wrinkles and speckles. However, when image is already small, pooling too much seems deteriorate the performance. Usually takes 2x2 shape and strides of 1x1. In VGG net, stride of both 1x1 and 2x2 were used, but when I tested on my 2-layer conv net, since my image was already small, bigger strides performed worse.

- Dropouts:
It's been said that dropout acts as regularization.

- Existence of a Batch Normalization layer after each conv layer:   
It is a good idea to have a batch normalization layer after conv layer to normalize weights for mini batches for each layer. It normalizes weights in each layer such that the weights after several layers with activations would not blow up, which happens more often as nets get deeper. It's been reported that having BN layers makes training easier without having to worry about careful initialization of weights and allows to use higher learning rates and sometimes eliminates need of dropouts. ([Read more..](http://jmlr.org/proceedings/papers/v37/ioffe15.pdf))

- Popular architecture:   
```INPUT -> [[CONV -> RELU]*N -> POOL?]*M -> [FC -> RELU]*K -> FC
```
, where 0<=N<=3, M >=0, K<3.  
When I tweak parameters for multi-layer cnn, I found it is also important to tweak gradient descending parameters such as learning rate, decay rate and momentum. I noticed that learning rate needed to be a lot lower for multi-layer model than single-layer model. Maybe I can use BN layer to see if it makes more robust on learning rate.

Without tweaking a lot, I was able to get 88% accuracy and precision for double-layer model.
My current test architecture is
CONV (64 3x3 filters, zero-padded)
CONV (64 3x3 filters, zero-padded)
MaxPool (2x2 kernel 1x1 stride)
output
with SGD parameters lr =E-4, decay=E-5, momentum =0.9
and batch size =2, n_epoch = 20

I found that increasing n_epoch and keeping everything else the same makes 89%, but I observed validation loss has gone up at some point as n_epoch increased which seems an overfitting.
It is weird that test accuracy is still going up nevertheless.
It may be because that data in train, validation and test are very similar.
I suspect that it maybe because 1 second sampling may include several signals in it so 1 second sampling of adjacent peak may contain the same neighbors thus some features are repeated throughout the whole data pool- this can happen when there are a bunch of peaks closely located each other in time domain (say, a dog barking furiously).
One idea to test if this is the case is that I can set aside files before I pooling 1-second signal segments such that train and test set never share the same recording.
