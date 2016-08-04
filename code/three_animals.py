from __future__ import division
import numpy as np
from numpy.random import choice
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
import os
from collections import Counter
from keras.regularizers import l1l2
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.utils import np_utils
from keras.optimizers import SGD

global DATADIR
global FOLDER

def load_data(testsplit=0.2, balance=True, size=1000):
    animal = {"cat":1,"dog":0, 'bird':2}
    X=[]
    y=[]
    for key in FOLDER.keys():
        directory = DATADIR+FOLDER[key]
        files = os.listdir(directory)
        Xi=[]

        if balance:
            files = choice(files, size)

        for fn in files:
            x = np.load(directory+fn)
            d = x.shape[2]-3*x.shape[1]
            d1 = int(round(d/2))
            d2 = d-d1
            xs = x.reshape((3*x.shape[1],x.shape[2]))[:,d1:x.shape[2]-d2]
            Xi.append(xs)
            yi = list(np.ones(len(Xi))*animal[key])

        X+=Xi
        y+=yi

    X = np.array(X)
    y = np.array(y).T

    X = np.array(X)
    y = np.array(y).T
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=testsplit)

    X_train, y_train = shaping(X_train,y_train)
    X_test, y_test = shaping(X_test,y_test)
    return X_train, X_test, y_train, y_test

def shaping(X,y):
    X_new = X.reshape((X.shape[0],1,X[0].shape[1],X.shape[2]))
    y_new = np_utils.to_categorical(y,3)
    return X_new, y_new

# class CNN(object):
#     def __init__
#         self.n_epoch = nb_epoch
#         self.batch_size = batch_size
#         self.n_filters = n_filters

def single_layer(X_train, X_test, y_train, y_test):
    model = Sequential()
    model.add(Convolution2D(nb_filter = 64, nb_row = 3, nb_col = 3, border_mode='valid',input_shape=(1, 36, 36)))
    model.add(Activation('relu'))
    model.add(Flatten())
    model.add(Dense(3))
    model.add(Activation('softmax'))

    sgd = SGD(lr=0.007, decay=0.01, momentum=0.9)
    model.compile(loss='categorical_crossentropy', optimizer='sgd')
    model.fit(X_train,y_train, batch_size=1, nb_epoch=15, verbose =1, validation_split=0.2)
    y_pred=model.predict_classes(X_test)

    print "Single 2d-conv net Result"
    print classification_report(y_test, y_pred)
    return model

def double_layer(X_train, X_test, y_train, y_test):
    model = Sequential()
    model.add(ZeroPadding2D((1,1),input_shape=(1, 36, 36)))
    model.add(Convolution2D(nb_filter = 128, nb_row = 3, nb_col = 3, border_mode='valid', activation = 'relu'))

    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(64, 3, 3, activation='relu'))

    model.add(MaxPooling2D((2,2), strides=(1,1)))
    model.add(Flatten())
    model.add(Dense(3))
    model.add(Activation('softmax'))

    sgd = SGD(lr=0.0001, decay=0.00001, momentum=0.9)
    model.compile(loss='categorical_crossentropy', optimizer='sgd')
    model.fit(X_train, y_train, batch_size=2, nb_epoch=10, verbose =1, validation_split=0.2)
    y_pred=model.predict_classes(X_test)
    print "Multipayer 2d-conv net Result"
    print classification_report(y_test, y_pred)
    return model

def ConvJS(X_train, X_test, y_train, y_test):
    model = Sequential()
    model.add(ZeroPadding2D((1,1),input_shape=(1, 36, 36)))
    model.add(Convolution2D(nb_filter = 64, nb_row = 3, nb_col = 3, border_mode='valid', activation = 'relu', init='glorot_normal'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(64, 3, 3, activation='relu',init='glorot_normal'))
    model.add(MaxPooling2D((2,2), strides=(1,1)))
    model.add(Dropout(0.25))

    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(nb_filter = 64, nb_row = 3, nb_col = 3, border_mode='valid', activation = 'relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(64, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(1,1)))
    model.add(Dropout(0.5))

    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(nb_filter = 32, nb_row = 3, nb_col = 3, border_mode='valid', activation = 'relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(32, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(1,1)))
    model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(3,init='glorot_normal'))
    model.add(Activation('softmax'))

    sgd = SGD(lr=0.01, decay=0.01, momentum=0.9)
    model.compile(loss='categorical_crossentropy', optimizer='sgd')
    model.fit(X_train,y_train, batch_size=2, nb_epoch=15, verbose =1, validation_split=0.2)
    y_pred=model.predict_classes(X_test)
    print "Multipayer 2d-conv net Result"
    print classification_report(y_test, y_pred)
    return model

if __name__=='__main__':
    DATADIR = '/home/geena/projects/which_animal/data/selected/nparrays/'
    FOLDER={'cat':'cat/dur1_win50_hop25_mfcc13/','dog':'dog/dur1_win50_hop25_mfcc13/','bird':'bird/dur1_win50_hop25_mfcc13/'}
    X_train, X_test, y_train, y_test = load_data(0.2)
    y_test = np.argmax(y_test,axis=1)


    # model1 = single_layer(X_train, X_test, y_train, y_test)
    # model2 = double_layer(X_train, X_test, y_train, y_test)
    model3 = ConvJS(X_train, X_test, y_train, y_test)
