import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time, urllib.request
import requests

PATH = r'C:\Users\antoi\Documents\chromedriver.exe'
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:\Users\antoi\Documents\chromedriver.exe' )

likes = []
followers_list = []
artists = []


def connect(name):


    driver.get("https://www.instagram.com/")
    time.sleep(5)
    try:
        notnow = driver.find_element_by_xpath("//button[contains(text(), 'Accepter tout')]").click()
    except NoSuchElementException:
        pass

    time.sleep(3)
    try:
        username = driver.find_element_by_css_selector("input[name='username']")
        password = driver.find_element_by_css_selector("input[name='password']")
        username.clear()
        password.clear()
        username.send_keys("FindYourTruck")
        password.send_keys("esgi2018")
        login = driver.find_element_by_css_selector("button[type='submit']").click()
    except NoSuchElementException:
        pass
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
    searchbox = driver.find_element_by_css_selector("input[placeholder='Rechercher']")
    searchbox.clear()
    searchbox.send_keys(name)
    time.sleep(5)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(3)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(3)
    followers = driver.find_element_by_xpath("/html/body/div[1]/div/div/section/main/div/header/section/ul/li[2]/a/span").text

    i = 0
    while(i < 2):
        followers_list.append(followers)
    time.sleep(2)


def first_picture():
    # finds the first picture
    pic = driver.find_element_by_class_name('_9AhH0')
    pic.click()


def like():
    time.sleep(2)
    try:
        like = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/a/span').text
        likes.append(like)
        time.sleep(2)
    except NoSuchElementException:
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
    while (i < 2):
        next_el = next_picture()

        # if next button is there then
        if next_el != False:
            artists.append(artist)
            # click the next button
            next_el.click()
            time.sleep(2)

            # like the picture
            like()
            time.sleep(2)
            i+=1
        else:
            print("not found")
            break


