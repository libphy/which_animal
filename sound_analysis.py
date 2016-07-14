# import cPickle as pickle
#
# with open('catlinks.pkl') as f:
#     catlinks = pickle.load(f)
# from collections import Counter
# fileX =map(lambda x: x.split('.')[-1],catlinks)
# Counter(fileX)
# #Out[10]: Counter({u'mp3': 48, u'pdf': 98})
# # it is depressing that it only has ~50 relevant files
# cat_mp3 = filter(lambda x: x.split('.')[-1]=='mp3', catlinks)

import urllib, os
os.chdir('data/cat')
for link in cat_mp3:
    testfile = urllib.URLopener()
    testfile.retrieve(link, link.split('=')[-1])
os.chdir('../..')
