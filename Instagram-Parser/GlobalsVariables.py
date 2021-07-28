from Imports import *

likes = []
followers_list = []
artists = []
date = []
type = []
views = []
description = []
listUrl = []
type_post =["Photo","Video","Reels"]
nbPostsToScrap = 10
url = "https://www.instagram.com/"
sTodayDate = datetime.now().strftime('%d/%m/%y')
fileName = datetime.now().strftime('%Y%m%d')
driverPath = "C:/Users/brand/Desktop/Projets perso/Projet music analytics/youtubeParser/driver/chromedriver.exe"
csvPath = "C:/Users/brand/Desktop/Projet datartist/Datartist/listArtistInsta.csv"
outPathParquet = "C:/Users/brand/Desktop/Projets perso/Projet music analytics/parquetFileInsta/"

