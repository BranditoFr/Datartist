import tst
from datetime import datetime

import pandas as pd
import selenium
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time, urllib.request
import requests
from pyspark.sql import SparkSession


# spark = SparkSession.builder.appName("appName").getOrCreate()
# sc = spark.sparkContext

chromeOptions = Options()
chromeOptions.headless = True
driver = webdriver.Chrome(r'C:\Users\antoi\Documents\chromedriver.exe', options=chromeOptions)

def current_time():
    return datetime.now().strftime('%Y-%m-%d')

csvFile = ["koba la d"]

#, "vald", "niska", "ash kidd", "hamza", "ateyaba", "djadja&dinaz", "PNL","gazo", "nekfeu", "nadirmusic", "jok'air", "kaaris", "kalash criminel", "jul", "naps", "jsx"
for artist in csvFile :

    tst.connect(artist)

    time.sleep(5)
    tst.first_picture(artist)

    tst.continue_like(artist)

    data = { 'artist':tst.artists, 'likes':tst.likes, 'followers':tst.followers_list}

print(data)
print(len(data))
finalData = pd.DataFrame(data)

finalData.to_csv(r'data/'+current_time()+'.csv')
print(finalData)

