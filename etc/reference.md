# Reference & Resource

### Data sources
1. [TierstimmenArchiv- animal sound archive (in German)](http://www.tierstimmenarchiv.de/webinterface/contents/treebrowser.php)
  - (ex1) [demostic dog](http://www.tierstimmenarchiv.de/webinterface/contents/querytext.php?mode=clearresults&querytext_1=Canis%20lupus%20f.%20familiaris&queryfield_1=species&querytype_1=matches&fields=1&startvalue=1)
  - (ex2) [domestic cat](http://www.tierstimmenarchiv.de/webinterface/contents/querytext.php?mode=clearresults&querytext_1=Felis%20silvestris%20f.%20domestica&queryfield_1=species&querytype_1=matches&fields=1&startvalue=1)

2. [Freesound.org database](https://www.freesound.org)

### Papers and thesis
1. [Animal sound classification thesis](https://www.ims.tuwien.ac.at/publications/tr-1882-038.pdf)    
Take-away: MFCC performs the best among various sound featurization techniques. First 7 MFCCs suffice to have 70+% recall and precision for cats, dogs, birds, and cows classification. Each category had around 100 sound file data. Analysis done in knn, svm, etc, but have not  been tried in neural network.  

2. [CNN for speech recognition](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/CNN_ASLPTrans2-14.pdf)  
Take-away: Mfcc arrays can be used as image input in CNN. Use the log-energy computed directly from the mel-frequency cepstral spectrum (without doing DCT- discrete cosine transform) rather than mfcc to preserve locality.

### Web articles about feature extraction methods
- [SR Wiki:  mfcc](http://recognize-speech.com/feature-extraction/mfcc#)   
- [web tutorial:  mfcc](http://practicalcryptography.com/miscellaneous/machine-learning/guide-mel-frequency-cepstral-coefficients-mfccs/)

### Useful tools
- [DSP python tools](https://github.com/AllenDowney/ThinkDSP) : Signal processing tools. I used it for sound data exploration.
- [librosa package](https://github.com/librosa/librosa) : Sound processing and featurization tools. I used it to calculate mfcc, delta, and delta2.
- [ffmpeg](https://ffmpeg.org/) : Converts audio/video file formats. I also used it for down-sampling audio signals.
- [mp3fy](www.mp3fy.com) : Youtube video to audio converter. Works well even with hours-long videos.  
