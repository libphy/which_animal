from bs4 import BeautifulSoup as BS
import requests
import dryscrape

mainpage = 'http://www.tierstimmenarchiv.de/webinterface/guest.php'
s = requests.Session()

res = s.get(mainpage)
cookies = dict(res.cookies)
url = 'http://www.tierstimmenarchiv.de/webinterface/contents/querytext.php?mode=clearresults&querytext_1=Felis%20silvestris%20f.%20domestica&queryfield_1=species&querytype_1=matches&fields=1&startvalue=1'
r=s.get(url,cookies=cookies)
soup = BS(r.text,'html')
datapglink = ['http://www.tierstimmenarchiv.de/webinterface/contents/'+x.find('a')['href'] for x in soup.findAll('tr',attrs={'class':"oddrow"})+soup.findAll('tr',attrs={'class':"evenrow"})]
# r2 = s.get(datapglink[0], cookies= cookies)
# soup2 = BS(r2.content,'html')
# soup2.findAll('form', attrs={'action': "http://www.tierstimmenarchiv.de/filedownload.php"})



import dryscrape
sess = dryscrape.Session()
sess.visit(datapglink[0])
response = sess.body()
soup = BeautifulSoup(response)
soup.findAll('form')
