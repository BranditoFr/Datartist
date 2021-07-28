from Imports import *
from GlobalsVariables import *

driver = webdriver.Chrome(driverPath)

# Function to check if a path exist in webpage
def checkExistsByXpath(driver,xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

# Connection to Instagram and get followers, today date
def connect(name):
    print("Info: Connexion à instagram.")
    driver.get(url)
    time.sleep(5)
    try:
        notnow = driver.find_element_by_xpath("//button[contains(text(), 'Accepter tout')]").click()
    except NoSuchElementException:
        pass
    time.sleep(3)
    try:
        username = driver.find_element_by_css_selector("input[name='username']")
        password = driver.find_element_by_css_selector("input[name='password']")
        username.clear()
        password.clear()
        username.send_keys("contact.eleskin@gmail.com")
        password.send_keys("azer123mdp")
        login = driver.find_element_by_css_selector("button[type='submit']").click()
    except NoSuchElementException:
        pass
    time.sleep(5)
    try:
        notnow = driver.find_element_by_xpath("//button[contains(text(), 'Plus tard')]").click()
    except NoSuchElementException:
        pass
    time.sleep(5)
    try:
        notnow2 = driver.find_element_by_xpath("//button[contains(text(), 'Plus tard')]").click()
    except NoSuchElementException:
        pass
    time.sleep(5)
    searchbox = driver.find_element_by_css_selector("input[placeholder='Rechercher']")
    time.sleep(1)
    searchbox.clear()
    time.sleep(1)
    searchbox.send_keys(name)
    time.sleep(5)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(3)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(5)
    print("before follow")
    if checkExistsByXpath(driver,'/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span') == True:
        follow = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span").get_attribute("title")
    print("end connect")
    return follow

# Finds the first picture
def first_picture(artist,followers):
    print("first_pic")
    time.sleep(5)
    try:
        pic = driver.find_element_by_class_name('_9AhH0')
        pic.click()
        like(artist,followers)
        next_picture()
        return False
    except NoSuchElementException:
        return True

# Get likes, views, and type of post (photo, video, reel)
def like(artist,followers):
    time.sleep(6)
    descr = ""
    if checkExistsByXpath(driver,'/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/a/span') == True:
        like = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/a/span').text
        likes.append(like)
        type.append(type_post[0])
        print("Info : This post is a photo.")
    elif checkExistsByXpath(driver,"/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/span/span") == True:
        view = driver.find_element_by_xpath("/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/span/span").text
        likes.append(view)
        type.append(type_post[1])
        print("Info : This post is a video.")
    elif checkExistsByXpath(driver,'/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div[2]/a/span') == True:
        reelLike = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div[2]/a/span').text
        likes.append(reelLike)
        type.append(type_post[2])
        print("Info : This post is a reel.")
    if checkExistsByXpath(driver, '/html/body/div[5]/div[2]/div/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span') == True :
        try:
            descr = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/div[1]/ul/div/li/div/div/div[2]/span').text
            print(descr)
        except NoSuchElementException:
            descr = ""
    time.sleep(5)
    description.append(descr)
    listUrl.append(driver.current_url)
    followers_list.append(followers)
    date.append(sTodayDate)
    artists.append(artist)

# Pass to next post
def next_picture():
    time.sleep(3)
    try:
        nextPost = driver.find_element_by_class_name("coreSpriteRightPaginationArrow")
        time.sleep(4)
        return nextPost
    except selenium.common.exceptions.NoSuchElementException:
        return 0

# Add elements to differents lists
def continue_like(artist,followers):
    i = 0
    while (i < nbPostsToScrap-1):
        next_el = next_picture()
        # if next button is there then
        if next_el != False:
            # click the next button
            next_el.click()
            time.sleep(4)
            like(artist,followers)
            i+=1
        else:
            print("Info : No more posts.")
            break


