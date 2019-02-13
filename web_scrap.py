#libraries

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup
import json
import re
import time as time

url = 'https://angel.co/automotive'

#setting chrome driver (with path to my local chromedriver)
driver = webdriver.Chrome("C:/webdrivers/chromedriver.exe")
driver.implicitly_wait(30)
driver.get(url)

infos = {}
count = 0
startups = []
for i in range(20):
    
    try:
        #--- automatic click on each startup that appears on the website ---#
        
        startups.append(driver.find_elements_by_class_name('startup-link'))
        next = startups[0][count]
        next.location_once_scrolled_into_view
        time.sleep(0.5)
        next.click()
        time.sleep(2)
        
        #--- getting important infos about desired startup ---#
        
        #not working
        photo_aux = driver.find_element_by_class_name('photo')
        #print(photo_aux.text)

        title_aux = driver.find_element_by_class_name('s-grid0-colMd14')
        title = re.split('\n', title_aux.text)
        
        locat_aux = driver.find_element_by_class_name('js-location_tag_holder')
        locat = locat_aux.text

        indus_aux = driver.find_element_by_class_name('js-market_tag_holder')
        indus = indus_aux.text

        emplo_aux = driver.find_element_by_class_name('js-company_size')
        emplo = emplo_aux.text

        #only works with one site (not all social medias)
        links_aux = driver.find_element_by_class_name('js-links')
        links = links_aux.text

        descr_aux = driver.find_element_by_class_name('content')
        descr = re.split('\n', descr_aux.text)

        #not working
        descr_hid_aux = driver.find_element_by_class_name('hidden')
        descr_hid = descr_hid_aux.text
        
        if len(title) == 1:
            infos[title[0]] = []
        else:
            infos[title[0]] = [title[1]]
        infos[title[0]].append(locat)
        infos[title[0]].append(indus)
        infos[title[0]].append(emplo)
        infos[title[0]].append(links)
        infos[title[0]].append(descr[1])
        
        time.sleep(0.5)
        driver.get(url)
        time.sleep(2)
        count += 2
        startups = []
        
        #--- clicking on the MORE button when it has visited all startups presents on the actual page ---#
        
        if count % 20 == 0 and count != 0:
            more_button = driver.find_element_by_class_name('hidden')
            time.sleep(0.5)
            more_button.location_once_scrolled_into_view
            more_button.click()
            time.sleep(2)
            
    except WebDriverException:
        print('error clicking')
    
driver.quit()

#saving all answers into a .json document

list_key_value = [[k,v] for k, v in infos.items()]
with open("startups.json", "w") as f:
    f.write(json.dumps(list_key_value))
