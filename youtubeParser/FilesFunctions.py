from Imports import *

## Extract artist and channel/username from csv
def csvToDf(csvPath):
    try:
        data        = pd.read_csv(csvPath,sep=';')
        dfFromCsv   = pd.DataFrame(data, columns= ['artist','channel','username'])
        return dfFromCsv
    except IOError:
        print("Erreur csvToDf: Le dataframe n'a pas pu être créé à partir du csv.")

##  Create file parquet
def dfToParquet(df,outPath):
    try:
        today       = datetime.date.today()
        path        = os.path.join(outPath, today.strftime('%Y%m%d'))
        os.mkdir(path)
        write("../parquetFile/"+today.strftime('%Y%m%d')+"/"+"youtube_artists.parquet", df)
        print("Info: Le fichier parquet a bien été créé.")
    except IOError:
        print("Erreur dfToParquet: Le fichier parquet n'a pas pu être créé suite à une erreur ou parce qu'il existe déjà.")