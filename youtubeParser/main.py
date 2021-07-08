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
## Launch spark session
# spark = SparkSession \
# .builder \
# .appName("Python Spark SQL basic example") \
# .getOrCreate()
# #Create PySpark DataFrame from Pandas
# sparkDF = spark.createDataFrame(dfFinal)
# sparkDF.printSchema()
# print(python_version())
# today = datetime.date.today()
# path = os.path.join(outPathParquet, today.strftime('%Y%m%d'))
# sparkDF.write.parquet(path)
# print("Info: Le fichier parquet a bien été créé.")

## End
print("Fin de la récupération des données Youtube.")




