import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time, urllib.request
import requests

PATH = r'C:\Users\antoi\Documents\chromedriver.exe'
# chromeOptions = Options()
# chromeOptions.headless = True
driver = webdriver.Chrome(r'C:\Users\antoi\Documents\chromedriver.exe')#, options=chromeOptions)

likes = []
followers_list = []
artists = []
date = []
def current_time():
    return datetime.now().strftime('%Y-%m-%d')

def connect(name):


    driver.get("https://www.instagram.com/")
    time.sleep(5)
    try:
        notnow = driver.find_element_by_xpath("//button[contains(text(), 'Accepter tout')]").click()
    except NoSuchElementException:
        pass

    time.sleep(3)


    username = driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input")
    password = driver.find_element_by_css_selector("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input")
    username.clear()
    password.clear()
    username.send_keys("FindYourTruck")
    password.send_keys("esgi2018")
    login = driver.find_element_by_css_selector("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button").click()

    time.sleep(5)
    try:
        notnow = driver.find_element_by_xpath("//button[contains(text(), 'Plus tard')]").click()
    except NoSuchElementException:
        pass
    time.sleep(5)
    try:
        notnow2 = driver.find_element_by_xpath("//button[contains(text(), 'Plus tard')]").click()
    except NoSuchElementException:
        pass

    time.sleep(5)
    searchbox = driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")
    time.sleep(1)
    searchbox.clear()
    time.sleep(1)
    searchbox.send_keys(name)
    time.sleep(5)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(3)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(3)
    followers = driver.find_element_by_xpath("/html/body/div[1]/div/div/section/main/div/header/section/ul/li[2]/a/span").get_attribute("title")

    i = 0
    while(i < 4):
        followers_list.append(followers)
        date.append(current_time())
        i+=1
    time.sleep(2)


def first_picture(artist):
    # finds the first picture
    artists.append(artist)

    pic = driver.find_element_by_class_name('_9AhH0')
    pic.click()
    exit = like()
    while (exit != 1 ):
        next_el = next_picture()
        time.sleep(2)
        if next_el != False:
            next_el.click()
            exit = like()
        else:
            break


def like():
    time.sleep(2)
    try:
        like = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/a/span').text
        likes.append(like)
        return 1
        time.sleep(2)
    except NoSuchElementException:
        return 0
        pass




def next_picture():
    time.sleep(2)
    try:
        nex = driver.find_element_by_class_name("coreSpriteRightPaginationArrow")
        time.sleep(1)
        return nex
    except selenium.common.exceptions.NoSuchElementException:
        return 0


def continue_like(artist):
    i = 0
    while (i < 3):
        next_el = next_picture()

        # if next button is there then
        if next_el != False:

            # click the next button
            next_el.click()
            time.sleep(2)

            # like the picture
            exit = like()
            time.sleep(2)
            if exit == 1:
                artists.append(artist)
                i+=1

        else:
            print("not found")
            break


