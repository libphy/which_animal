from bs4 import BeautifulSoup as BS
import requests
import cPickle as pickle
import urllib, os
from collections import Counter

mainpage = 'http://www.tierstimmenarchiv.de/webinterface/guest.php'
s = requests.Session()
res = s.get(mainpage)
cookies = dict(res.cookies)


def get_pages(url, lastpg): #returns list of item pages
    pages=[]
    for i in range(int(lastpg)):
        pgurl = url[:-1]+str(i+1)
        r_i=s.get(pgurl,cookies=cookies) #This website needs cookie to access other pages.
        soup_i = BS(r_i.text,'html')
        pages += ['http://www.tierstimmenarchiv.de/webinterface/contents/'+x.find('a')['href'] for x in soup_i.findAll('tr',attrs={'class':"oddrow"})+soup_i.findAll('tr',attrs={'class':"evenrow"})]
    return pages

def get_download_links(pglinks, s, cookies): #extracts a download link from an item page
    links=[]
    errors=[]
    for i in range(len(pglinks)):
        r2 = s.get(pglinks[i], cookies= cookies)
        soup2 = BS(r2.content,'xml')
        try:
            fname = soup2.findAll('div',attrs={'class':"toolbar"})[0].findAll('form')[0].findAll('form',attrs={'method':"POST",'target':"_blank"})[0]['action']
            links.append('http://www.tierstimmenarchiv.de/webinterface/contents/'+fname)
            print 'item '+str(i+1)+' OK'
        except IndexError:
            errors.append(i)
            print 'item '+str(i+1)+' Fail'
    return links, errors
# This website sometimes has blank files and will throw an error, or rejects a request even there is a file for no reason.
# so the function 'get_download_links' keeps track of indices that have failed downloading,
# then the function 'datalinks_species' loops it over failed links for 5 iterations or less.
def datalinks_species(url):
    r0=s.get(url,cookies=cookies)
    soup0 = BS(r0.text,'html')
    lastpg = soup0.findAll('table')[-1].findAll('input')[-1]['value']
    datapglinks = get_pages(url,lastpg)
    print len(datapglinks), ' files'
    batch = datapglinks
    failedbatch=[]
    downloadlinks=[]
    i=0
    while i<5 and len(failedbatch)<len(datapglinks):
        print 'iteration: ', i
        links_success, failed_index = get_download_links(batch, s, cookies)
        failedbatch = map(lambda i: batch[i],failed_index)
        downloadlinks += links_success
        batch = failedbatch
        i+=1
    print len(downloadlinks), ' success from ', len(datapglinks), ' results'
    return downloadlinks

def downloadfiles(linkslist, downloaddir, path2pkl=None):
    """
        linkslist: <iterable> a list of full download links. Will be ignored when pickle path is given.
        downloaddir: <folder path> a direcory where downloaded files will be saved.
        path2pkl: <file path> a file path to a saved download links pickle file.
    """
    if path2pkl not None:
        with open(path2pkl) as f:
            links = pickle.load(f)
    else:
        links = linkslist
    # This website sometimes gives a blank pdf files when soundfile download button is clicked
    # thus I need to check a file extension.
    # This website only has .mp3 type audio files.
    link_mp3 = filter(lambda x: x.split('.')[-1]=='mp3', links)
    cwd = os.getcwd()
    os.chdir(downloaddir)
    i=0
    l=len(link_mp3)
    for link in link_mp3:
        print i,'/',l
        testfile = urllib.URLopener()
        testfile.retrieve(link, link.split('=')[-1])
        i+=1

    os.chdir(cwd)
    print 'Done'

if __name__ == '__main__':
    # At the time of writing this code, I visited the tierstimmen website (in German) and navigated to get url for domestic cats, then used python requests library.
    # Later I wrote another code that can navigate to search animals using selenium to download annotation csv file.
    # Below is an example
    urldict = {'cat':'http://www.tierstimmenarchiv.de/webinterface/contents/querytext.php?mode=clearresults&querytext_1=Felis%20silvestris%20f.%20domestica&queryfield_1=species&querytype_1=matches&fields=1&startvalue=1',
    'dog':'http://www.tierstimmenarchiv.de/webinterface/contents/querytext.php?querytext_2=Canis+lupus+f.+familiaris&sel_2=Haushund&sel_3=Domestic+dog&queryfield_2=species&querytype_2=matches&querytext_1=&queryfield_1=description&querytype_1=contains&fields=2&startvalue=1'}
    cat_url = urldict['cat']
    catlinks = datalinks_species(cat_url)
    #####(optional) saving/loading pickle
    # with open( "catlinks.pkl", "w" ) as f:
    #     pickle.dump(catlinks, f)
    # with open( "catlinks.pkl") as f:
    #     catlinks = pickle.load(f)
    #####
    directory = '/home/geena/projects/which_animal/data/scrape/tierstimmen/cat'
    downloadfiles(catlinks, directory)
