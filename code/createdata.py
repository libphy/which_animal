from __future__ import division
import numpy as np
import cPickle as pickle
import pandas as pd
import librosa
import math
import os

global DATADIR
global PKLDICT

def createdata(key, fft_win=25,fft_hop=10,**kwargs):
    """Create mfcc matrix dataset for all files associated anumal key
    fft_win: fft window width in ms when calculating mfcc (default: 25)
    fft_hop: fft slide in ms when calculating mfcc (default: 10)
    [More args customizabl in the subfuction windowcut]
    dur: slice width of a time series signal in second (default: 1)
    discard_short: discard the time series data if it's shorter than slice width you want (default: True).
    """
    subdir = '_'.join(['dur'+str(kwargs['dur']).replace('.','p'),'win'+str(fft_win).replace('.','p'),'hop'+str(fft_hop).replace('.','p')])
    destdir = DATADIR+'nparrays/'+key+'/'+subdir+'/'
    print destdir
    if not os.path.exists(destdir):
        os.makedirs(destdir)


    ext = '.npy'
    with open(DATADIR+PKLDICT[key]) as f:
        df = pickle.load(f)

    for fn, tulist in zip(df['filename'],df['active_region']):
        y,sr = librosa.load(DATADIR+key+'/'+fn)
        yn = y/(abs(y).max())
        k=0

        for tu in tulist:
            i=int(tu[0])
            j=int(tu[1])
            yseg = windowcut(yn,i,j,sr=sr,**kwargs)
            mfcc = librosa.feature.mfcc(y=yseg, sr=sr, n_fft = round(fft_win/1000*sr), hop_length=round(fft_hop/1000*sr)) # 25 ms width and 10 ms slide
            mfcc_delta = librosa.feature.delta(mfcc)
            mfcc_delta2 = librosa.feature.delta(mfcc, order=2)
            res = np.array([mfcc,mfcc_delta,mfcc_delta2])
            savename = '_'.join([fn.split('.')[0],'k'+str(k)])
            np.save(destdir+savename+ext,res)
            k+=1
    print 'Done'

def windowcut(y,i,j,dur=1,sr=22050,discard_short=True):
    """ Returns a slice of y with a specified width
    dur: width of window in second
    """
    if dur < len(y)/sr:
        left = round((i+j)/2)-round(dur*sr/2)
        right = left+round(dur*sr)
        if left<0:
            left = 0
            right = round(dur*sr)
        elif right>len(y):
            right = len(y)
            left = right -  round(dur*sr)
        return y[int(left):int(right)]
    else: #discard data if total length is smaller than duration we want
        if discard_short:
            return None
        else: #padd with zeros at the end
            return np.append(y,np.zeros(round(dur*sr)-len(y)))



if __name__ =='__main__':

    DATADIR = '/home/geena/projects/which_animal/data/selected/'

    PKLDICT={'cat':'cat_slice_new.pkl','dog':'dog_slice_new.pkl'}
    createdata('cat',dur=1,discard_short = False, fft_win=25,fft_hop=10)
