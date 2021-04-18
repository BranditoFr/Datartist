from googleapiclient.discovery import build
import pandas as pd

youTubeApiKey = "AIzaSyDFF2AjGVG1WwZW8uCgo5yQtr16-rrv5aQ"
youtube = build('youtube','v3', developerKey=youTubeApiKey)
channelId = "UCNtD7oDVld6YeaYV7tCXo1A"

statdata=youtube.channels().list(part='statistics',id=channelId).execute()
stats=statdata['items'][0]['statistics']
## Get count of subscribers in suscriberCount variable
suscriberCount=stats['subscriberCount']
suscriberCount

snippetdata=youtube.channels().list(part='snippet',id=channelId).execute()
## Get the channel name in channel variable
channel=snippetdata['items'][0]['snippet']['title']
channel

## Get All the video details in variable video
contentdata=youtube.channels().list(id=channelId,part='contentDetails').execute()
playlist_id = contentdata['items'][0]['contentDetails']['relatedPlaylists']['uploads']
videos = []
next_page_token = None

while 1:
    res = youtube.playlistItems().list(playlistId=playlist_id,
                                    part='snippet',
                                    maxResults=20,
                                    pageToken=next_page_token).execute()
    videos += res['items']
    next_page_token = res.get('nextPageToken')

    if next_page_token is None:
        break

video_ids = list(map(lambda x:x['snippet']['resourceId']['videoId'], videos))
stats = []
for i in range(0, len(video_ids), 40):
    res = (youtube).videos().list(id=','.join(video_ids[i:i+40]),part='statistics').execute()
    stats += res['items']



title=[]
datetime=[]
liked=[]
disliked=[]
views=[]
##url=[]
comment=[]
nbVideos = 10
if len(videos) < 10 :
    nbVideos = len(videos)
else:
    for i in range(nbVideos):
        title.append((videos[i])['snippet']['title'])
        datetime.append((videos[i])['snippet']['publishedAt'])
        ##url.append("https://www.youtube.com/watch?v="+(videos[i])['snippet']['resourceId']['videoId'])
        liked.append(int((stats[i])['statistics']['likeCount']))
        disliked.append(int((stats[i])['statistics']['dislikeCount']))
        views.append(int((stats[i])['statistics']['viewCount']))
        comment.append(int((stats[i])['statistics']['commentCount']))


data = {'channel': channel, 'title': title, 'datetime': datetime, 'liked': liked, 'disliked': disliked,
            'views': views, 'comment': comment, 'followers': suscriberCount}
df = pd.DataFrame(data)
print(df)