from __future__ import division
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
import os
from collections import Counter
from keras.regularizers import l1l2
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers.core import Dense, Dropout, Activation, Flatten, Merge, Reshape, MaxoutDense
from keras.utils import np_utils
from keras.optimizers import SGD

global DATADIR
global FOLDER

def load_data(testsplit=0.2, setaside=False, asc=False):
    animal = {"cat":1,"dog":0}
    X=[]
    y=[]
    Xs=[]
    ys=[]
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
        if setaside:
            if asc:
                # setaside first consecutive files
                cutind = int(len(Xi)*testsplit)
                Xs+=Xi[:cutind]
                ys+=yi[:cutind]
                X+=Xi[cutind:]
                y+=yi[cutind:]
            else:
                #set aside last consecutive files
                cutind = -1*int(len(Xi)*testsplit)
                X+=Xi[:cutind]
                y+=yi[:cutind]
                Xs+=Xi[cutind:]
                ys+=yi[cutind:]
        else:
            X+=Xi
            y+=yi

    X = np.array(X)
    y = np.array(y).T
    if setaside: #setaside needs separate shuffling for each
        Xs = np.array(Xs)
        ys = np.array(ys).T
        Xy= zip(X,y)
        Xys= zip(Xs,ys)#np.array(map(lambda i: [Xs[i],ys[i]],range(len(ys))))
        np.random.shuffle(Xy)
        np.random.shuffle(Xys)
        X_train= np.array(map(lambda x: x[0],Xy))
        y_train= np.array(map(lambda x: x[1],Xy))
        X_test= np.array(map(lambda x: x[0],Xys))
        y_test= np.array(map(lambda x: x[1],Xys))
    else:
        X = np.array(X)
        y = np.array(y).T
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=testsplit)

    X_train, y_train = shaping(X_train,y_train)
    X_test, y_test = shaping(X_test,y_test)
    return X_train, X_test, y_train, y_test

def shaping(X,y):
    X_new = X.reshape((X.shape[0],1,X[0].shape[1],X.shape[2]))
    y_new = np_utils.to_categorical(y,2) # y_new[:,0] are inverted, y_new[:,1] are original
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
    model.add(Dense(2))
    model.add(Activation('softmax'))

    sgd = SGD(lr=0.007, decay=0.01, momentum=0.9)
    model.compile(loss='categorical_crossentropy', optimizer='sgd')
    model.fit(X_train,y_train, batch_size=1, nb_epoch=15, verbose =1, validation_split=0.2)
    y_pred=model.predict_classes(X_test)

    print "Single 2d-conv net Result"
    print classification_report(y_test[:,1], y_pred)
    return model

def double_layer(X_train, X_test, y_train, y_test):
    model = Sequential()
    model.add(ZeroPadding2D((1,1),input_shape=(1, 36, 36)))
    model.add(Convolution2D(nb_filter = 128, nb_row = 3, nb_col = 3, border_mode='valid', activation = 'relu'))

    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(64, 3, 3, activation='relu'))

    model.add(MaxPooling2D((2,2), strides=(1,1)))
    model.add(Flatten())
    model.add(Dense(2))
    model.add(Activation('softmax'))

    sgd = SGD(lr=0.0001, decay=0.00001, momentum=0.9)
    model.compile(loss='categorical_crossentropy', optimizer='sgd')
    model.fit(X_train,y_train, batch_size=2, nb_epoch=10, verbose =1, validation_split=0.2)
    y_pred=model.predict_classes(X_test)
    print "Multipayer 2d-conv net Result"
    print classification_report(y_test[:,1], y_pred)
    return model

def ConvJS(X_train, X_test, y_train, y_test):
    model = Sequential()
    model.add(ZeroPadding2D((1,1),input_shape=(1, 36, 36)))
    model.add(Convolution2D(nb_filter = 64, nb_row = 3, nb_col = 3, border_mode='valid', activation = 'relu', init='glorot_normal'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(64, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(1,1)))
    model.add(Dropout(0.25))

    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(nb_filter = 64, nb_row = 3, nb_col = 3, border_mode='valid', activation = 'relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(64, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(1,1)))
    model.add(Dropout(0.25))

    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(nb_filter = 32, nb_row = 3, nb_col = 3, border_mode='valid', activation = 'relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(32, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(1,1)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(2,init='glorot_normal'))
    model.add(Activation('softmax'))

    sgd = SGD(lr=0.001, decay=0.01, momentum=0.9)
    model.compile(loss='categorical_crossentropy', optimizer='sgd')
    model.fit(X_train,y_train, batch_size=2, nb_epoch=15, verbose =1, validation_split=0.2)
    y_pred=model.predict_classes(X_test)
    print "Multipayer 2d-conv net Result"
    print classification_report(y_test[:,1], y_pred)
    return model

if __name__=='__main__':
    DATADIR = '/home/geena/projects/which_animal/data/selected/nparrays/rescaling_each/'
    FOLDER={'cat':'cat/dur1_win50_hop25_mfcc13/','dog':'dog/dur1_win50_hop25_mfcc13/'}
    X_train, X_test, y_train, y_test = load_data(0.2)
    # X_train-=np.mean(X_train,axis=0)
    # X_test-=np.mean(X_test,axis=0)
    model = ConvJS(X_train, X_test, y_train, y_test)

    # model2 = Sequential()
    # model2.add(Convolution2D(nb_filter = 64, nb_row = 3, nb_col = 3, weights=model.layers[0].get_weights(), border_mode='valid',input_shape=(1, X.shape[2], X.shape[3])))
    # model2.add(Activation('relu'))
    # activations = model2._predict(X_batch)

    # directory = DATADIR+FOLDER['cat']
    # files = sorted(os.listdir(directory))
