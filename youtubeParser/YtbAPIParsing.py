from GlobalsVariables import *
from SeleniumScraper import getAllVideosFromChannel
from Imports import *

def getDataFromYtbAPI(df):
    ## Build youtube api instance
    youtube = build('youtube', 'v3', developerKey=youTubeApiKey)
    ## Loop for iterate on each artist
    for index, row in df.iterrows():
        ## Declare variables
        scraperWithoutAPI   = False
        noRelatedPlaylist   = False
        user                = row['username']
        channelId           = row['channel']
        stats               = []
        videos              = []

        ## Get different categories of informations (statistics, snippet, content) about artists by channel id or username
        if user != "Null":
            statdata = youtube.channels().list(part='statistics', forUsername=user).execute()
            snippetdata = youtube.channels().list(part='snippet', forUsername=user).execute()
            contentdata = youtube.channels().list(part='contentDetails', forUsername=user).execute()
        else:
            statdata = youtube.channels().list(part='statistics', id=channelId).execute()
            snippetdata = youtube.channels().list(part='snippet', id=channelId).execute()
            contentdata = youtube.channels().list(part='contentDetails', id=channelId).execute()
        ## Get total subscriber
        statist = statdata['items'][0]['statistics']
        ## Get playlist Id to get the video details in variable videos
        playlistId = contentdata['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        nextPageToken = None

        while 1:
            ## Try catch for artist who don't have related playlists
            try:
                res = youtube.playlistItems().list(playlistId=playlistId,
                                                   part='snippet',
                                                   maxResults=50,
                                                   pageToken=nextPageToken).execute()
                videos += res['items']
                nextPageToken = res.get('nextPageToken')
                if nextPageToken is None:
                    break

            except errors.HttpError:
                print("Info Youtube API: L'artiste " + row['artist'] + "  n'a pas de playlist associée.")
                noRelatedPlaylist = True
                break

        ## If artist haven't related playlist or not enough videos in related playlist, we use scraping without API to get all videos from artist
        if noRelatedPlaylist == True or len(videos) < nbVideosToScrap:
            print("Info: Lancement du script d'automatisation pour l'artiste " + row['artist'] + ".")
            scraperWithoutAPI = True
            videos = []
            if user != "Null":
                ## Function need username/channel for artist, boolean to know if it's channel or username, nb videos to scrap, and path for driver(chrome for exemple)
                ## getAllVideos return tuple, list of videos and list of urls of this videos
                listVideos, listUrl = getAllVideosFromChannel(user, False, nbVideosToScrap, driverPath)
            else:
                listVideos, listUrl = getAllVideosFromChannel(channelId, True, nbVideosToScrap, driverPath)

            for i in range(0, len(listVideos)):
                res = (youtube).videos().list(id=listVideos[i], part='statistics').execute()
                stats += res['items']
                res1 = (youtube).videos().list(id=listVideos[i], part='snippet').execute()
                videos += res1['items']
        else:
            ## Get lists of videos ids
            video_ids = list(map(lambda x: x['snippet']['resourceId']['videoId'], videos))

            for i in range(0, len(video_ids), 40):
                res = (youtube).videos().list(id=','.join(video_ids[i:i + 40]), part='statistics').execute()
                stats += res['items']

        ## Check if the nb of videos match with our global variable
        nbVideos = nbVideosToScrap
        if len(videos) < nbVideos:
            nbVideos = len(videos)
        ## Get content of each videos
        for i in range(nbVideos):
            ## Get count of subscribers in suscriberCount variable
            suscriberCount.append(statist['subscriberCount'])
            ## Get the channel name in channel variable
            channel.append(snippetdata['items'][0]['snippet']['title'])
            title.append((videos[i])['snippet']['title'])
            sTemp = ((videos[i])['snippet']['publishedAt']).replace("T"," ")
            date_video.append(sTemp.replace("Z",""))
            if scraperWithoutAPI == False:
                url.append("https://www.youtube.com/watch?v=" + (videos[i])['snippet']['resourceId']['videoId'])
            else:
                url.append(listUrl[i])
            liked.append(int((stats[i])['statistics']['likeCount']))
            disliked.append(int((stats[i])['statistics']['dislikeCount']))
            views.append(int((stats[i])['statistics']['viewCount']))
            comment.append(int((stats[i])['statistics']['commentCount']))
            lArtistsNames.append(row['artist'])

    ## Put our data list in Dataframe and return df
    data    = {'artist_name':lArtistsNames,'date':todayDate,'channel': channel, 'title': title, 'date_video': date_video, 'liked': liked, 'disliked': disliked,
            'views': views, 'comment': comment, 'followers': suscriberCount, 'url': url}
    return pd.DataFrame(data)