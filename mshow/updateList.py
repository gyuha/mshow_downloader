import os
from bs4 import BeautifulSoup

from mshow.imagesDownload import pathName
from mshow.driver import driver_init, driver_close
from mshow.dataSave import loadJsonFile

LIST_URL = "https://mangashow.me/bbs/board.php?bo_table=msm_manga&page=%d"

# 다운받은적 있는지 무식하게 찾는다
def existDownload(folerList, title):
    title = pathName(title)
    for downloaded in folerList:
        if downloaded in title:
            data = loadJsonFile(os.path.join("download", downloaded, "data.json"))
            return data["title"]
    return ""


# 만화책에서 제목을 보고 업데이트 목록을 가져 옴
def filterDownloadedList(folerList, driver, page):
    driver.get(LIST_URL%page)
    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")
    updateList = []
    try:
        subjects = bs.find("div", {"class", "list-container"}).find_all("div", {"class", "subject"})
        for subject in subjects:
            title = subject.text.splitlines()[1].strip()
            downloaed = existDownload(folerList, title)
            if downloaed != "":
                updateList.append(downloaed)
    except:
        pass
    return updateList

# 만화책 업데이트 목록 가져 오기 
def getUpdateList(updateSize = 3):
    folerList = os.listdir("download")
    driver = driver_init()
    list = []
    for i in range(1, updateSize + 1):
        print("[%d / %d] Download update list"%(i, updateSize), end="\r")
        downed = filterDownloadedList(folerList, driver, i)
        list = list + downed
    num = 0
    print("")
    print("Updated : %d"%len(list))
    for l in list:
        num = num + 1
        print("   %d. %s"%(num, l))
    driver_close(driver)
    return list
