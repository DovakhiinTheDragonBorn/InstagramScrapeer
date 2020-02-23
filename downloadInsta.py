from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException 
from bs4 import BeautifulSoup
from login import credentials
from time import sleep
import requests
from requests.exceptions import MissingSchema
import os



def download_image(imageHTML,i):
    imageSoup = BeautifulSoup(imageHTML,'lxml')
    imageTag = imageSoup.find('img',srcset=True)
    imageSource = imageTag['src']
        
    if imageTag:
        try:
            route = 'Data/'+targetUser+'/'+str(i)+'.jpg'
            f = open(route,'wb')
            f = open(''+targetUser+'/'+str(i)+'.jpg','wb')
            f.write(requests.get(imageSource).content)
            f.close()
            print(route + " Downloaded")
            return True
        except MissingSchema:
            print('Missing Schema')
            f.close()
            os.remove(route)
            return False

targetUser=input('UserName: @')
driver = webdriver.Chrome('C:\\WebDrivers\\chromedriver.exe')
driver.get('https://www.instagram.com/')
delay=10

if not os.path.exists(targetUser):
    os.makedirs(targetUser)

anchors = []
links = []
try:
    WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.XPATH,'//a[contains(text(),"Log in")]'))).click()
    sleep(2)
    WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.XPATH,'//input[@name="username"]'))).send_keys(credentials[0])
    WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.XPATH,'//input[@name="password"]'))).send_keys(credentials[1])
    WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.XPATH,'//button[@type="submit"]'))).click()
    WebDriverWait(driver,delay).until(EC.presence_of_element_located((By.XPATH,'//button[contains(text(),"Not Now")]'))).click()
    # sleep(5)
    driver.get('https://www.instagram.com/'+targetUser)


    scroll_pause_time = 2
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        html = driver.page_source

        soup = BeautifulSoup(html,'lxml')
        anchors=soup.find_all('a',href=True)
        for anchor in anchors:
            if anchor['href'].startswith('/p/'):
                if anchor['href'] not in links:
                    links.append(anchor['href'])

    i=0
    for link in links:
        driver.get('https://www.instagram.com'+link)
        imageHTML = driver.page_source
        if download_image(imageHTML,i):
            i=i+1
        while True:
            try:
                WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH,'//div[@class="coreSpriteRightChevron"]'))).click()
                imageHTML = driver.page_source
                if download_image(imageHTML,i):
                    i=i+1
            except TimeoutException:
                break


except TimeoutException:
    print('Page took too long to load') 
