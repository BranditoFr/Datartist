## pip install google-api-python-client
from GlobalsVariables import *
from SeleniumScraper import getAllVideosFromChannel
from FilesFunctions import *
from Imports import *
from YtbAPIParsing import getDataFromYtbAPI

## Launch
print("Lancement de l'application Youtube Parser...")
## Extract artists and channels/usernames from csv file
dfStart = csvToDf(inPathArtists)
## Get data from youtube API (and selenium scraper if necessary)
dfFinal = getDataFromYtbAPI(dfStart)
print(dfFinal.to_string())


## Create file parquet
dfToParquet(dfFinal,outPathParquet)
## End
print("Fin de la récupération des données Youtube.")



