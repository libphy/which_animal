from bs4 import BeautifulSoup as BS
import requests
import cPickle as pickle
from selenium import webdriver
import os
import subprocess

global USERNAME = os.getenv('FREESOUND_ID')
global PASSWORD = os.getenv('FREESOUND_PW')
global FIREFOX_USER_PF =  os.getenv('FIREFOX_USER_PF_FREESOUND') #path to a special user preference setting of firefox browser (to download media files without asking agreement)
global CHROME_WEBDRIVER = os.getenv('CHROME_WEBDRIVER')

def getlinks(keyword): #scrape download links in freesound.org using the search keyward (e.g. meow). Also filters out irrelevant ones using filefilter function
    mainpage = 'http://freesound.org/search/?q='+keyword
    s = requests.Session()
    res = s.get(mainpage)
    cookies = dict(res.cookies)
    r = s.get(mainpage,cookies=cookies)
    soup = BS(r.text,'html')
    lastpg = int(soup.find('li',attrs={'class':'last-page'}).find('a').text)
    itemlinks=[]
    for page in range(lastpg):
        pageurl = mainpage+'&page='+str(page+1)+'#sound'
        r_i = s.get(pageurl,cookies=cookies)
        soup_i = BS(r_i.text,'html')
        listings = soup_i.findAll('div',attrs={'class':'sound_title'})
        selected = filefilter(listings,blockwords(keyword))
        print str(len(selected))+'/'+str(len(listings)), ' files collected from page '+str(page)
        itemlinks += selected

    downloadlinks=[]
    for item in itemlinks:
        r1 = s.get(item)
        soup1 = BS(r1.text,'html')
        downloadlinks.append('http://freesound.org'+soup1.find('div',attrs={'id':'download'}).find('a')['href'])
    print len(downloadlinks), 'links found'
    return downloadlinks

def blockwords(key): #returns a list of block words for the search keyword
    if key == 'meow':
        # This list is used temporarily to filter some files irrelevant (or poorly tagged) for my search term 'meow'.
        # User should use their own filter (or none) that fits their purpose.
        fake = ['human','my voice','speed','loop','synth','transform','alter','distort','stereo','instrument','doppler','mix','simulate','ring','tone','electric','effect','imitated','manipulate','imitating','fake','speak']
        othernoise = ['background','dog','bark','child','people','scratch','ambient','ambience','city','car','eating','feeding','rain','water','clap','jungle','bird']
        stupid = ['mom','nya','silly','crazy','wife','mystery','school','paw','me meowing','me making','play','box','creepy','iphone','compilation','video','shadow','ailien','space']
        ambiguity = ['purr','hiss','heat','wildcat','fight','squeal','squeak','nervous','scream','irritated','fear','growl','howl']
    return fake + othernoise + stupid + ambiguity

def filefilter(listings, blocklist):
    rightlinks=[]
    for item in listings:
        title = item.find('a', attrs={'class':'title'}).text #title
        description = item.find('p', attrs={'class':'description'}).text
        tags = ' '.join(item.find('ul', attrs={'class':'tags'}).text.split())
        all_texts = title +' '+ description +' '+ tags
        if sum(map(lambda x: x in all_texts.lower(), blocklist)) == 0:
            rightlinks.append('http://freesound.org'+item.find('a',attrs={'class':'title'})['href'])
    return rightlinks

def testlogin(browser=None): #testing loging in selenium+firefox and selenium+chrome. Firefox needs cumtom profile setup for auto-download
    if browser == 'firefox':
        #Firefox needs profile setup for automatic download for certain types of files
        profile = webdriver.FirefoxProfile(FIREFOX_USER_PF)
            ###############################
            ## to create a firefox profile: https://support.mozilla.org/en-US/kb/profile-manager-create-and-remove-firefox-profiles
            ## to find profile path: https://support.mozilla.org/en-US/kb/back-and-restore-information-firefox-profiles#w_locate-your-profile-folder
            ######## alternative method but it did not work on my mac
            # profile = webdriver.FirefoxProfile()
            # profile.set_preference('browser.download.folderList', 2)
            # profile.set_preference('browser.download.manager.showWhenStarting', False)
            # profile.set_preference('browser.download.dir', os.getcwd())
            # profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'audio/wav')
            # profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'audio/mpeg')
            # profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'audio/aiff')
            # profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/ogg')
            #########
            ################################
        driver = webdriver.Firefox(profile)
    elif browser == 'chrome':
        #Chrome downloads without asking.
        driver = webdriver.Chrome(CHROME_WEBDRIVER)
    else:
        #Use default firefox browser (empty preference)
        driver = webdriver.Firefox()
    loginpg = 'http://freesound.org/home/login/?next=/'
    driver.get(loginpg)
    user = driver.find_element_by_name('username')
    user.click()
    user.send_keys(USERNAME)
    pwrd = driver.find_element_by_name('password')
    pwrd.click()
    pwrd.send_keys(PASSWORD)
    driver.find_element_by_xpath("//input[@value='login'][@type='submit']").click()
    return driver

def download(downloadlinks,soundtag): #download audio file contents (log-in required) using selenium+chromedriver
    ## chrome browser launch
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : os.getcwd()+'/data/freesound/'+soundtag}
    chromeOptions.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(executable_path=CHROME_WEBDRIVER, chrome_options=chromeOptions)
    ## freesound.org log in
    loginpg = 'http://freesound.org/home/login/?next=/'
    driver.get(loginpg)
    user = driver.find_element_by_name('username')
    user.click()
    user.send_keys(USERNAME)
    pwrd = driver.find_element_by_name('password')
    pwrd.click()
    pwrd.send_keys(PASSWORD)
    driver.find_element_by_xpath("//input[@value='login'][@type='submit']").click()
    i=0
    for filelink in downloadlinks:
        driver.get(filelink)
        i+=1

    print str(i)+' files downloaded'

def rename(directory,tag): #rename audio files and save the name change log as pickle
    fileslist = os.listdir(directory)
    newfileslist=map(lambda i: tag+ '_' + str(i) + '.' + fileslist[i].split('.')[1],range(len(fileslist)))
    log = zip(fileslist,newfileslist)
    with open( 'renamed_'+tag+'.pkl', "w" ) as f:
        pickle.dump(log, f)
    print directory
    for old, new in log:
        os.rename(directory+'/'+old,directory+'/'+new)
    print 'rename done'

def convert2wav(directory): # convert non-.wav audio files to .wav files using ffmpeg
    audioformats = ['mp3','flac','ogg','aiff','aif']
    fileslist = os.listdir(directory)
    bashCommandlist = filter(None,map(lambda name: 'ffmpeg -i '+ directory + '/'+ name + ' -ar 22050 -ac 1 '+ directory+'/'+ name.split('.')[0]+'.wav' if str(name.split('.')[1]) in audioformats else None, fileslist))
    for command in bashCommandlist:
        subprocess.check_output(['bash','-c', command])
    print '.wav convert done'

def movewavfiles(subdirectory): #move all .wav files into a subfolder named wav.
    # example: movewavfiles('data/freesound/test')
    cwd = os.getcwd()
    if not os.path.isdir(subdirectory+'/wav'):
        os.makedirs(subdirectory+'/wav')
    command = 'mv '+cwd+'/'+subdirectory+'/*.wav '+cwd+'/'+subdirectory+'/wav/'
    print command
    subprocess.check_output(['bash','-c', command])
    print 'wav files moved'
    print 'current directory: ', os.getcwd()

if __name__ == '__main__':

    links = getlinks('meow')
    ######### (optional) save to /load from pickle
    # with open( "cat_freesound.pkl", "w" ) as f:
    #     pickle.dump(links, f)
    # with open("cat_freesound.pkl") as f:
    #     links =  pickle.load(f)
    #########
    download(links,'meow')

    # rename('data/freesound/meow','meow_fs')
    # convert2wav('data/freesound/meow')
    # movewavfiles('data/freesound/meow')

    #rename('data/tierstimmen_cat','cat_ts')
    #convert2wav('data/tierstimmen_cat')
    #movewavfiles('data/tierstimmen_cat')
