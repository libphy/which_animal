import cPickle as pickle
import urllib, os
from collections import Counter

def downloadfiles(key):
    with open(key+'links.pkl') as f:
        links = pickle.load(f)
    fileX =map(lambda x: x.split('.')[-1],links)
    print Counter(fileX)
    link_mp3 = filter(lambda x: x.split('.')[-1]=='mp3', links)
    os.chdir('data/'+key)
    i=0
    l=len(link_mp3)
    for link in link_mp3:
        print i,'/',l
        testfile = urllib.URLopener()
        testfile.retrieve(link, link.split('=')[-1])
        i+=1
    os.chdir('../..')
    print 'Done'
# for cat
#Out[10]: Counter({u'mp3': 48, u'pdf': 98})
# it is depressing that it only has <50 relevant files

if __name__ == '__main__':
    downloadfiles('dog')
