from Imports import *
from GlobalsVariables import *

listArtist = []
try:
    data = pd.read_csv(csvListArtist, sep=';')
    dfFromCsv = pd.DataFrame(data, columns=['artists'])
except IOError:
    print("Erreur csvToDf: Le dataframe n'a pas pu être créé à partir du csv.")

for index, row in dfFromCsv.iterrows():
    listArtist.append(row['artists'])
##getChannelIntoCsv(listArtists)
driver = webdriver.Chrome(driverPath)
driver.get("https://www.youtube.com/")
time.sleep(5)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, pathPopUp1))).click()
with open('../listArtists.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    for artist in listArtist:
        driver.find_element_by_xpath("//input[@id='search']").clear()
        search = driver.find_element_by_xpath("//input[@id='search']")
        search.send_keys(artist)
        search.send_keys(Keys.RETURN)
        time.sleep(5)
        WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,
                                                                    "/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-renderer"))).click()
        time.sleep(5)
        url = driver.current_url
        spl_user = "/user/"
        spl_channel = "/channel/"
        if url.find(spl_user) != -1:
            row = (artist, "Null", url.partition(spl_user)[2])
            writer.writerow(row)
            time.sleep(5)
        if url.find(spl_channel) != -1:
            row = (artist, url.partition(spl_channel)[2], "Null")
            writer.writerow(row)
            time.sleep(5)
    print(open('../listArtists.csv', 'rt').read())
    outfile.close()
driver.close
