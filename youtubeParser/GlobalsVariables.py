from Imports import *
## Globals variables
listToDF        = []
suscriberCount  = []
channel         = []
title           = []
date_video      = []
liked           = []
disliked        = []
views           = []
url             = []
comment         = []
lArtistsNames   = []
todayDate       = (datetime.date.today()).strftime('%Y%m%d')
## Set nb videos we want scrap
nbVideosToScrap = 10
## File contain the list of artist with channel/username
inPathArtists   = "C:/Users/brand/Desktop/Projets perso/Projet music analytics/listArtist.csv"
## Out path to create parquet file from dataframe artists
outPathParquet  = "C:/Users/brand/Desktop/Projets perso/Projet music analytics/parquetFile/"
csvListArtist   = "C:/Users/brand/Desktop/Datartist/listArtist.csv"
## Youtube API key
youTubeApiKey   = "AIzaSyDFF2AjGVG1WwZW8uCgo5yQtr16-rrv5aQ"
## Driver path (chrome)
driverPath      = "C:/Users/brand/Desktop/Projets perso/Projet music analytics/youtubeParser/driver/chromedriver.exe"
pathPopUp1      = "/html/body/div/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button/span"
pathPopUp2      = "/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/ytd-mealbar-promo-renderer/div/div[2]/ytd-button-renderer[1]/a/tp-yt-paper-button/yt-formatted-string"