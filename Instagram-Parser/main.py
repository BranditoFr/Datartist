import tst
import pandas as pd
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time, urllib.request
import requests

driver = webdriver.Chrome(r'C:\Users\antoi\Documents\chromedriver.exe')

csvFile = ["booba", "koba la d"]

#, "vald", "niska", "ash kidd", "hamza", "ateyaba", "djadja&dinaz", "PNL","gazo", "nekfeu", "nadirmusic", "jok'air", "kaaris", "kalash criminel", "jul", "naps", "jsx"
for artist in csvFile :

    tst.connect(artist)

    time.sleep(5)
    tst.first_picture()
    tst.like()

    tst.continue_like(artist)

    data = { 'artist':tst.artists, 'likes':tst.likes, 'followers':tst.followers_list}


finalData = pd.DataFrame(data)

print(finalData)

