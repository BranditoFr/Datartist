##  pip install google-api-python-client
import pandas as pd
import numpy as np
import fastparquet
import datetime
import os
from fastparquet import write
from datetime import date
from googleapiclient.discovery import build
from googleapiclient import discovery, errors
from pprint import pprint

## Globals variables
listToDF        = []
suscriberCount  = []
channel         = []
title           = []
datetime        = []
liked           = []
disliked        = []
views           = []
url             = []
comment         = []
inPathArtists   = r"C:\Users\brand\Desktop\Projets perso\Projet music analytics\listArtist.csv"
outPathParquet  = "C:/Users/brand/Desktop/Projets perso/Projet music analytics/youtubeParser/"
youTubeApiKey   = "AIzaSyDFF2AjGVG1WwZW8uCgo5yQtr16-rrv5aQ"
youtube         = build('youtube','v3', developerKey=youTubeApiKey)

## Extract artist and channel/username from csv
data            = pd.read_csv(inPathArtists,sep=';')
dfFromCsv       = pd.DataFrame(data, columns= ['artist','channel','username'])

## Loop for iterate on each artist
for index,row in dfFromCsv.iterrows():
    if row['username'] != "Null":
        statdata    = youtube.channels().list(part='statistics',forUsername=row['username']).execute()
        snippetdata = youtube.channels().list(part='snippet', forUsername=row['username']).execute()
        contentdata = youtube.channels().list(part='contentDetails',forUsername=row['username']).execute()
    else:
        statdata    = youtube.channels().list(part='statistics',id=row['channel']).execute()
        snippetdata = youtube.channels().list(part='snippet',id=row['channel']).execute()
        contentdata = youtube.channels().list(part='contentDetails', id=row['channel']).execute()

    ## Get total subscriber
    statist         = statdata['items'][0]['statistics']

    ## Get All the video details in variable video
    playlist_id     = contentdata['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    videos          = []
    next_page_token = None

    while 1:
        ## try catch for artist who don't have relatedplaylists
        try :
            res             = youtube.playlistItems().list(playlistId=playlist_id,
                                           part='snippet',
                                           maxResults=50,
                                           pageToken=next_page_token).execute()
            videos          += res['items']
            next_page_token  = res.get('nextPageToken')

            if next_page_token is None:
                break

        except errors.HttpError:
            pprint("Erreur : L'artiste "+row['artist']+"  n'a pas de playlist associée.")
            break

    ##Get lists of videos ids
    video_ids   = list(map(lambda x: x['snippet']['resourceId']['videoId'], videos))
    ##Get stats of artists
    stats       = []

    for i in range(0, len(video_ids), 40):
        res     = (youtube).videos().list(id=','.join(video_ids[i:i + 40]), part='statistics').execute()
        stats   += res['items']
    nbVideos    = 10

    ##Get content of each videos
    if len(videos) < nbVideos:
        nbVideos = len(videos)

    for i in range(nbVideos):
        ## Get count of subscribers in suscriberCount variable
        suscriberCount.append(statist['subscriberCount'])
        ## Get the channel name in channel variable
        channel.append(snippetdata['items'][0]['snippet']['title'])
        title.append((videos[i])['snippet']['title'])
        datetime.append((videos[i])['snippet']['publishedAt'])
        url.append("https://www.youtube.com/watch?v="+(videos[i])['snippet']['resourceId']['videoId'])
        liked.append(int((stats[i])['statistics']['likeCount']))
        disliked.append(int((stats[i])['statistics']['dislikeCount']))
        views.append(int((stats[i])['statistics']['viewCount']))
        comment.append(int((stats[i])['statistics']['commentCount']))

data    = {'channel': channel, 'title': title, 'datetime': datetime, 'liked': liked, 'disliked': disliked,'views': views, 'comment': comment, 'followers': suscriberCount,'url':url}
df      = pd.DataFrame(data)
print(df.to_string())


##Create file parquet
today       = date.today()
path        = os.path.join(outPathParquet, today.strftime('%d%m%Y'))
os.mkdir(path)
write(today.strftime('%d%m%Y')+"/"+today.strftime('%d%m%Y')+'_youtube_artists.parquet', df)



