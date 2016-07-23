import cPickle as pickle
from selenium import webdriver
import os
from time import sleep

global CHROME_WEBDRIVER = os.getenv('CHROME_WEBDRIVER')

def download_anno(url,destination):
    #my linux desktop
    prefs = {"download.default_directory" : destination}
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(executable_path=CHROME_WEBDRIVER, chrome_options=chromeOptions)

    driver.get(url)
    query1 = driver.find_element_by_xpath("//select[@name='querytext_2']/option[text()='Canis lupus f. familiaris']").click()
    driver.find_element_by_xpath("//input[@value='suchen'][@type='submit']").click()
    sleep(5)
    #first page download
    driver.find_element_by_xpath("//input[@name='headbox'][@type='checkbox'][@onclick='checkall()']").click()
    driver.find_element_by_xpath("//input[@type='submit'][@name='toolbutton'][@value='CSV']").click()
    lastpg = int(driver.find_elements_by_xpath("//input[@type='submit'][@class='list'][@name='startvalue']")[-1].get_attribute('value'))
    driver.find_element_by_xpath("//input[@type='submit'][@class='list'][@name='startvalue'][@value='2']").click()
    sleep(5)
    #looping for next page download
    for i in xrange(3,lastpg+1):
        driver.find_element_by_xpath("//input[@name='headbox'][@type='checkbox'][@onclick='checkall()']").click()
        driver.find_element_by_xpath("//input[@type='submit'][@name='toolbutton'][@value='CSV']").click()
        driver.find_element_by_xpath("//input[@type='submit'][@class='list'][@name='startvalue'][@value={}]".format("'"+str(i)+"'")).click()
        sleep(5)
    #last page download
    driver.find_element_by_xpath("//input[@name='headbox'][@type='checkbox'][@onclick='checkall()']").click()
    driver.find_element_by_xpath("//input[@type='submit'][@name='toolbutton'][@value='CSV']").click()
    print 'download csv done'

if __name__=='__main__':
    dogurl = 'http://www.tierstimmenarchiv.de/webinterface/guest.php'
    saveto = '/home/geena/projects/which_animal/data/scrape/tierstimmen/test'
    download_anno(dogurl,saveto)
