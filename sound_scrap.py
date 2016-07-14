from bs4 import BeautifulSoup as BS
import requests
import cPickle as pickle

mainpage = 'http://www.tierstimmenarchiv.de/webinterface/guest.php'
s = requests.Session()
res = s.get(mainpage)
cookies = dict(res.cookies)


def get_pages(url, lastpg): #returns list of item pages
    pages=[]
    for i in range(int(lastpg)):
        pgurl = url[:-1]+str(i+1)
        r_i=s.get(pgurl,cookies=cookies)
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

if __name__ == '__main__':
    urldict = {'cat':'http://www.tierstimmenarchiv.de/webinterface/contents/querytext.php?mode=clearresults&querytext_1=Felis%20silvestris%20f.%20domestica&queryfield_1=species&querytype_1=matches&fields=1&startvalue=1',
    'dog':'http://www.tierstimmenarchiv.de/webinterface/contents/querytext.php?querytext_2=Canis+lupus+f.+familiaris&sel_2=Haushund&sel_3=Domestic+dog&queryfield_2=species&querytype_2=matches&querytext_1=&queryfield_1=description&querytype_1=contains&fields=2&startvalue=1&mode=query'}
    # cat_downloadlinks = datalinks_species(cat_url)
    # with open( "catlinks.pkl", "w" ) as f:
    #     pickle.dump(cat_downloadlinks, f)
    dog_downloadlinks = datalinks_species(urldict['dog'])
    with open( "doglinks.pkl", "w" ) as f:
         pickle.dump(dog_downloadlinks, f)
