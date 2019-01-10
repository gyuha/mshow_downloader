import os
from bs4 import BeautifulSoup
from collections import OrderedDict

from mshow.imagesDownload import pathName
from mshow.driver import driver_init, driver_close
from mshow.dataSave import loadJsonFile
from mshow.driver import retry_wait

LIST_URL = "https://mangashow.me/bbs/board.php?bo_table=msm_manga&page=%d"

# 다운받은적 있는지 무식하게 찾는다
def existDownload(folerList, title):
    title = pathName(title)
    for downloaded in folerList:
        if downloaded in title:
            data = loadJsonFile(os.path.join("download", downloaded, "data.json"))
            if not data:
                return ""
            if "title" in data:
                return data["title"]
    return ""

def parseList(folerList, driver):
    updateList = []
    try:
        html = driver.page_source
        bs = BeautifulSoup(html, "html.parser")

        subjects = bs.find("div", {"class", "list-container"}).find_all("div", {"class", "subject"})
        for subject in subjects:
            if subject.text.strip() == "":
                continue
            lines = subject.text.splitlines()
            if len(lines) < 1:
                continue
            title = lines[1].strip()
            downloaded = existDownload(folerList, title)
            if downloaded != "":
                updateList.append(downloaded)
    except Exception as e: 
        print(e)
        return updateList
    return updateList

# 만화책에서 제목을 보고 업데이트 목록을 가져 옴
def filterDownloadedList(folerList, driver, page):
    driver.get(LIST_URL%page)
    print(LIST_URL%page)

    updateList = parseList(folerList, driver)

    if len(updateList) == 0:
        retry_wait(7, "[업데이트목록] ")
        updateList = parseList(folerList, driver)
        if len(updateList) == 0:
            return filterDownloadedList(folerList, driver, page)

    return updateList

# 만화책 업데이트 목록 가져 오기 
def getUpdateList(driver, updateSize = 3):
    folerList = os.listdir("download")
    updateList = []
    for i in range(1, updateSize + 1):
        print("[%d / %d] Download update list"%(i, updateSize), end="\r")
        downed = filterDownloadedList(folerList, driver, i)
        updateList = updateList + downed
    updateList = list(set(updateList))
    num = 0
    print("")
    print("Updated : %d"%len(updateList))
    for l in updateList:
        num = num + 1
        print("   %d. %s"%(num, l))
    return updateList
