# which_animal

This project is about animal sound recognition using convolutional neural network. Convolutional neural network has been a popular tool in image recognition but recently has been implemented also in human speech recognition. Using image features from sound data is done by creating a collection of spectrum in a short time scale.

 Mel frequency cepstrum is a short-term power spectrum of a sound which represent a logarithmic energy in each frequency band in non-linear Mel scale to approximate the human auditory system's respond to a sound. The amplitudes of the envelops of the power spectrum are the coefficients called Mel-frequency cepstral coefficients (MFCCs) and are one of the most popular feature extraction methods in speech recognition.

## Data Scraping and Cleaning
I scraped data from the two websites below:
1. [TierstimmenArchiv](http://www.tierstimmenarchiv.de/webinterface/contents/treebrowser.php) : an animal sound research archive in Germany
2. [Freesound.org](https://www.freesound.org) : a crowd-sourced database on sounds and sound effects

Tierstimmenachiv is an animal sound database for researchers. They have sound data from variety of animals including birds, domestic mammals, wild mammals, amphibians, reptiles, and more. I chose cats and dogs because I thought they would be fun, but later I realized that cat and dog sound data is hard to find as opposed to bird sound data which outnumbers all other animal sounds because of ornithology.  I scraped data using Selenium and Requests, and got 50 files for cat sounds and 120 for dog sounds after filtering blank pdf files they had in the data download links.   

Since cat data was not enough I scraped more files from freesound.org website. Freesound had over 300 listings for the search keyword 'meow'. However the quality of the data was not as good as Tierstimmen, since it had many mis-categorized data such as human voice recordings imitating a cat sound or sound effects that are mixed with cat sounds. I wrote a script to parse texts from title, description, and tags of the listings and applied word filtering to get rid of those wrong files, then I manually corrected some of the tags for data from Freesound. Tierstimmen also has sound descriptions written in German, so I wrote a script to extract and translate the sound keywords.

Then I used Pandas, matplotlib, ipython widgets, IPython display and Audio for further data cleaning and data exploration process.

## Feature Extraction

## Models

## Results

## Reference & Resource

### References
1. Matthias Zeppelzauer, Discrimination and retrieval of animal sounds. Technischen Universit ̈at Wien, Thesis (2005).
Take-away: MFCC performs the best among various sound featurization techniques. First 7 MFCCs suffice to have 70+% recall and precision for cats, dogs, birds, and cows classification. Each category had around 100 sound file data. Analysis done in knn, svm, etc, but have not  been tried in neural network.  

2. Ossama Abdel-Hamid et. al., Convolutional Neural Networks for Speech Recognition., EEE/ACM Transactions on Audio, Speech, and Language Processing, Vol 22 (10), pp 1533-1545 (2014)

3. Sergey Ioffe & Christian Szegedy, Batch normalization: Accelerating deep network training by reducing internal covariate shift., arXiv:1502.03167 (2015)

4. Nitish Srivastava et.al., Dropout: a simple way to prevent neural networks from overfitting., Journal of Machine Learning Research, Vol. 15 (1), pp.1929-1958 (2014)

5. Xavier Clorot & Yoshua Bengio, Understanding the difficulty of training deep feedforward neural networks. JMLR Proceedings of AISTATS, Vol. 9, pp.249-256 (2010)

6. [Stanford CS231n resources](http://cs231n.github.io/)

7. Michael Lutter, [Mel Frequency Cepstral Coefficients](http://recognize-speech.com/feature-extraction/mfcc#)., SR Wiki  (web)
8. Blog post, [Mel Frequency Cepstral Coefficients Tutorial](http://practicalcryptography.com/miscellaneous/machine-learning/guide-mel-frequency-cepstral-coefficients-mfccs/), Practical cryptography (web)

### Useful tools
- [DSP python tools](https://github.com/AllenDowney/ThinkDSP) : Signal processing tools. I used it for sound data exploration.
- [librosa package](https://github.com/librosa/librosa) : Sound processing and featurization tools. I used it to calculate mfcc, delta, and delta2.
- [ffmpeg](https://ffmpeg.org/) : Converts audio/video file formats. I also used it for down-sampling audio signals.
- [mp3fy](www.mp3fy.com) : Youtube video to audio converter. Works well even with hours-long videos.  
