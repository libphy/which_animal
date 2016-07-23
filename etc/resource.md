# Galvanize Project General
## Zipian projects  
[Zipfian projects repo](https://github.com/zipfian/project-proposals)  
[Past student projects](https://github.com/zipfian/project-proposals/blob/master/past_student_projects.md)

## Data sources  
[kaggle data](www.kaggle.com/datasets)  
[kaggle competitions](www.kaggle.com/competitions)  
[reddit](www.reddit.com/r/bigquery/wiki/datasets)      
[Amazon](aws.amazon.com/public-data-sets/)  
[Github](github.com/caesar0301/awesome-public-datasets)  
[Quora](www.quora.com/Where-can-I-find-large-datasets-open-to-the-public)  
[Stanford](snap.stanford.edu/data/)

# My Project Resources
## Trained nets (image recognition)
[VGG19](https://gist.github.com/baraldilorenzo/8d096f48a1be4a2d660d)

## Previous students project repos (image recognition)
[ChefNet](https://github.com/Mikelew88/ChefNet)  by Mike Lewis  
[Nikki ]
[Accent]https://github.com/dwww2012/Accent-Classifier

## Animal sounds data sources

#### sources to use
[German animal sound repo](http://www.tierstimmenarchiv.de/webinterface/contents/treebrowser.php)
- (ex1) [demostic dog 717 results](http://www.tierstimmenarchiv.de/webinterface/contents/querytext.php?mode=clearresults&querytext_1=Canis%20lupus%20f.%20familiaris&queryfield_1=species&querytype_1=matches&fields=1&startvalue=1)
- (ex2) [domestic cat](http://www.tierstimmenarchiv.de/webinterface/contents/querytext.php?mode=clearresults&querytext_1=Felis%20silvestris%20f.%20domestica&queryfield_1=species&querytype_1=matches&fields=1&startvalue=1)

[Free sound database](https://www.freesound.org)
libphy/yahoo/qp

#### others
[Macualay library- animal sounds (mostly birds)](http://macaulaylibrary.org/search-help)  
http://www.soundboard.com/sb/Dog_Sounds_sound  
http://soundbible.com/tags-dog-bark.html  
[Soundsnap (pay to download)](http://www.soundsnap.com/tags/barking)   

#### youtube sources
https://www.youtube.com/watch?v=P9AY5rc5M28
https://www.youtube.com/watch?v=ljYzRXlPEUo
[youtube downloader code](https://github.com/nficano/pytube)


## References
#### papers and thesis
[animal sound classification thesis](https://www.ims.tuwien.ac.at/publications/tr-1882-038.pdf)    
Take-away: MFCC performs the best. first 7 MFCC suffice to have 70+% recall and precision for cats, dogs, birds, and cows classification. each category had <100 data. analysis done in knn, svm, etc, but not neural network.  

[speech recog using cnn](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/CNN_ASLPTrans2-14.pdf)  
Take-away: use the log-energy computed directly from the mel-frequency spectral coefficients (there is a problem with using mfcc ?)  

[Audio-Visual Speech Recognition using SciPy](http://conference.scipy.org/proceedings/scipy2010/pdfs/reikeras.pdf)  
shows how to use scipy tools for mfcc  

#### Articles
[MFCC](http://recognize-speech.com/feature-extraction/mfcc#[object%20HTMLHeadingElement])    
[CNN for speech recognition](http://recognize-speech.com/acoustic-model/knn/comparing-different-architectures/convolutional-neural-networks-cnns#[object%20HTMLHeadingElement])    
[DSP](http://greenteapress.com/thinkdsp/html/index.html)
[mfcc](http://practicalcryptography.com/miscellaneous/machine-learning/guide-mel-frequency-cepstral-coefficients-mfccs/) 

#### Tools
[DSP python tools](https://github.com/AllenDowney/ThinkDSP)
[python_speech_features](https://github.com/jameslyons/python_speech_features)
[scikits talkbox- mfcc](https://github.com/cournape/talkbox/blob/master/scikits/talkbox/features/mfcc.py)
[librosa](https://github.com/librosa/librosa) :  can calculate mfcc, delta, delta2
[Hmm.. another tool? (even has regression tools)](http://journals.plos.org/plosone/article/asset?id=10.1371/journal.pone.0144610.PDF)
