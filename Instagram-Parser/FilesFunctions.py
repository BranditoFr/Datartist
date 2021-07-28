from Imports import *
from GlobalsVariables import *

## Extract artist and channel/username from csv
def csvToDf(csvPath):
    try:
        data        = pd.read_csv(csvPath,sep=';')
        dfFromCsv   = pd.DataFrame(data, columns= ['artists'])
        return dfFromCsv
    except IOError:
        print("Error csvToDf: Dataframe can't be create with csv.")

##  Create file parquet
def dfToParquet(df,outPath):
    try:
        path        = os.path.join(outPath, fileName)
        os.mkdir(path)
        write(outPath+fileName+"/"+"insta_artists.parquet", df)
        print("Info: Parquet file successfully create.")
    except IOError:
        print("Error dfToParquet: File can't be create.")