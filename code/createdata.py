from __future__ import division
import numpy as np
import cPickle as pickle
import pandas as pd
import librosa
import math
import os

global DATADIR
global PKLDICT
global DESTDIR

def createdata(key, **kwargs):
    """Create mfcc matrix dataset for all files associated anumal key
    INPUT
        fft_win: fft window width in ms when calculating mfcc (default: 25)
        fft_hop: fft slide in ms when calculating mfcc (default: 10)

    More args customizabl in the subfuction windowcut
        dur: slice width of a time series signal in second (default: 1)
        discard_short: discard the time series data if it's shorter than slice width you want (default: True).
    """
    duration = kwargs['dur']
    fft_win = kwargs['fft_win']
    fft_hop = kwargs['fft_hop']
    n_mfcc = kwargs['n_mfcc']


    subdir = '_'.join(['dur'+str(duration).replace('.','p'),'win'+str(fft_win).replace('.','p'),'hop'+str(fft_hop).replace('.','p'), 'mfcc'+str(n_mfcc)])
    DESTDIR = DATADIR+'nparrays/'+key+'/'+subdir+'/'

    if not os.path.exists(DESTDIR):
        os.makedirs(DESTDIR)

    ext = '.npy'
    with open(DATADIR+PKLDICT[key]) as f:
        df = pickle.load(f)

    for fn, tulist in zip(df['filename'],df['active_region']):
        y, sr = librosa.load(DATADIR+key+'/'+fn)
        yn = y/(abs(y).max())
        k=0
        n_fft = int(round(fft_win/1000*sr))
        hop_length = int(round(fft_hop/1000*sr))
        for tu in tulist:
            i=int(tu[0])
            j=int(tu[1])
            if j-i <= round(duration*sr):
                yseg = windowcut(yn,i,j,sr=sr,dur=duration, discard_short = kwargs['discard_short'])
                savename = '_'.join([fn.split('.')[0],'k'+str(k)])
                savemfcc(savetarget = DESTDIR+savename+ext, y=yseg, sr=sr, n_mfcc=n_mfcc, n_fft = n_fft, hop_length = hop_length)
            else:
                m=0
                cut = lambda x: (2*x+1)*round(duration*sr/2)
                slices = filter(None,map(lambda n: (int(i+cut(n)-cut(0)),int(i+cut(n)+cut(0))) if i+cut(n)<j else None, range(int(math.ceil(duration*sr)))))
                for tu in slices:
                    ii=int(tu[0])
                    jj=int(tu[1])
                    yseg = windowcut(yn,ii,jj,sr=sr,dur=duration, discard_short = kwargs['discard_short'])
                    savename = '_'.join([fn.split('.')[0],'k'+str(k)+'_'+'m'+str(m)])
                    # print DESTDIR+savename+ext
                    savemfcc(savetarget = DESTDIR+savename+ext, y=yseg, sr=sr, n_mfcc=n_mfcc, n_fft = n_fft, hop_length = hop_length)
                    m+=1
            k+=1
    print 'Done'


def savemfcc(savetarget, y, sr, n_mfcc,  **kwargs):
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc, **kwargs)
    mfcc_delta = librosa.feature.delta(mfcc)
    mfcc_delta2 = librosa.feature.delta(mfcc, order=2)
    # ALthough a test showed not much difference, by eye, it seems rescaling each is better.
    #rescale each matrix
    res = np.array([rescale(mfcc[1:]),rescale(mfcc_delta[1:]),rescale(mfcc_delta2[1:])])
    #rescale all at once (deltas will be squeezed since mfcc has larger scales)
    #res = rescale(np.array([mfcc[1:],mfcc_delta[1:],mfcc_delta2[1:]]))
    np.save(savetarget,res)

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
            return np.array(np.append(y,np.zeros(round(dur*sr)-len(y))))

def rescale(m):
    #rescale by global max of absolute values
    offset = m.min()
    scale = m.max()-m.min()
    return (m-offset)/scale



if __name__ =='__main__':

    DATADIR = '/home/geena/projects/which_animal/data/selected/'
    PKLDICT={'cat':'cat_slice_new.pkl','dog':'dog_slice_new.pkl'}
    createdata('cat',dur=1,discard_short = False, fft_win=50,fft_hop=25, n_mfcc=13)
    createdata('dog',dur=1,discard_short = False, fft_win=50,fft_hop=25, n_mfcc=13)
