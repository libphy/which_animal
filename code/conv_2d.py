from __future__ import division
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
import os
from collections import Counter
#np.random.seed(1337)  # for reproducibility
# from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
# from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.layers.core import Dense, Dropout, Activation, Flatten, Merge, Reshape, MaxoutDense
from keras.utils import np_utils
from keras.optimizers import SGD

global DATADIR
global FOLDER

def load_data():
    animal = {"cat":1,"dog":0}
    X=[]
    y=[]
    for key in FOLDER.keys():
        directory = DATADIR+FOLDER[key]
        files = os.listdir(directory)
        Xi=[]
        for fn in sorted(files):
            x = np.load(directory+fn)
            d = x.shape[2]-3*x.shape[1]
            d1 = int(round(d/2))
            d2 = d-d1
            xs = x.reshape((3*x.shape[1],x.shape[2]))[:,d1:x.shape[2]-d2]
            Xi.append(xs)
            yi = list(np.ones(len(Xi))*animal[key])
        X+=Xi
        y+=yi
    return np.array(X), np.array(y).T

# class CNN(object):
#     def __init__

if __name__=='__main__':
    DATADIR = '/home/geena/projects/which_animal/data/selected/nparrays/rescaling_all_at_once/'
    FOLDER={'cat':'cat/dur1_win50_hop25_mfcc13/','dog':'dog/dur1_win50_hop25_mfcc13/'}
    X0, y0 = load_data()
    X = X0.reshape((X0.shape[0],1,X0.shape[1],X0.shape[2]))
    y = np_utils.to_categorical(y0,2)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    model = Sequential()
    model.add(Convolution2D(nb_filter = 64, nb_row = 3, nb_col = 3, border_mode='valid',input_shape=(1, X.shape[2], X.shape[3])))
    model.add(Activation('relu'))
    model.add(Flatten())
    model.add(Dense(2))
    model.add(Activation('softmax'))

    sgd = SGD(lr=0.007, decay=0.01, momentum=0.9)
    model.compile(loss='categorical_crossentropy', optimizer='sgd')
    model.fit(X_train,y_train, batch_size=1, nb_epoch=100)
    y_pred=model.predict_classes(X_test)
    # np_util's [1] is the original for binary case
    # print "y_pred: ", Counter(y_pred)
    # a = Counter(y_test[:,1]==y_pred)
    # print "accuracy:", a[True]/(a[False]+a[True])
    print "Result"
    print classification_report(y_test[:,1], y_pred)
