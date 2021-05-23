from Imports import *
from GlobalsVariables import *

## Web scraping using selenium (automatisation tool)

## Function to check if a path exist in webpage
def checkExistsByXpath(driver,xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

## Function allow to get all videos from a given channel or username (id) and a boolean isChannel to check it's channel or username, return list of all videos
def getAllVideosFromChannel(id,isChannel,nbOfVideos,path):
    ## Declare variables
    baseVideoUrl    = 'https://www.youtube.com/'
    channel         = 'channel/'
    user            = 'user/'
    driver          = webdriver.Chrome(path)
    listUrl         = []
    ## Check if we have channel id or username
    if isChannel == False:
        driver.get(baseVideoUrl + user + id + '/videos')
    else:
        driver.get(baseVideoUrl + channel + id + '/videos')
    time.sleep(5)
    ## Pass pop-up
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, pathPopUp1))).click()
    time.sleep(5)
    count       = 0
    listVideos  = []
    ## Loop while we find videos
    while (count <= nbOfVideos):
        count   = count + 1
        if checkExistsByXpath(driver,'/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer[' + str(count) + ']/div[1]/div[1]') == True:
            time.sleep(5)
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                    '/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer[' + str(
                                                                        count) + ']/div[1]/div[1]'))).click()
                time.sleep(10)
                url = driver.current_url
                listUrl.append(driver.current_url)
                splitVideos = "/watch?v="
                if url.find(splitVideos) != -1:
                    listVideos.append(url.partition(splitVideos)[2])
                driver.back()
                time.sleep(5)
            except WebDriverException:
                print("Warning 'getAllVideosFromChannel': La vidéo n'est pas cliquable.")
                ## Check if pop up 'no thanks' appear and click if true
                if checkExistsByXpath(driver,pathPopUp2) == True:
                    try:
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,pathPopUp2))).click()
                        time.sleep(5)
                    except WebDriverException:
                        print("Warning 'getAllVideosFromChannel': Pop-up contenant 'non merci' n'est pas cliquable.")
        else:
            break
    ## Close driver and return list of videos
    driver.close
    return listVideos, listUrl

