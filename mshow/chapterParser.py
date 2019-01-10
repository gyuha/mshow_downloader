import os
import pathlib
import time

from bs4 import BeautifulSoup
from mshow.imagesDownload import imagesDownload, pathName
from mshow.dataSave import saveJsonFile, loadJsonFile
from mshow.driver import retry_wait

DOWNLOAD_FOLDER = "download"
BASE_URL = 'https://mangashow.me/bbs/board.php?bo_table=msm_manga&wr_id='


def saveFolderPath(titlePath, chapter, num):
    chapter = pathName(chapter)
    path = os.path.join(titlePath, "%03d" % (num,) + "-" + pathName(chapter))
    return path

# 만화책에서 이미지 목록을 가져 와서 다운로드 하기
def chapterImages(driver, title, data):
    titlePath = os.path.join(DOWNLOAD_FOLDER, pathName(title))

    pathlib.Path(titlePath).mkdir(parents=True, exist_ok=True)
    skip_num = 0
    saveData = loadJsonFile(os.path.join(titlePath, "data.json"))
    if saveData:
        skip_num = int(saveData["skip"])
    
    num = 1
    for d in data:
        url = BASE_URL + d["wr_id"]
        if skip_num >= num:
            print("[" + str(num) + "/" + str(len(data)) + "] 패스 : " + d["title"] )
            num = num + 1
            continue
        savePath = saveFolderPath(titlePath, d["title"], num)
        print("[" + str(num) + "/" + str(len(data)) + "] 다운로드 : " + d["title"])
        num = num + 1
        if os.path.exists(savePath + ".zip"):
            print("이미 압축한 파일 :" + d["title"])
            continue
        print("Get image list by url..", end="\r")

        images = getImageList(driver, url )
        print("Download images..      ", end="\r")

        imagesDownload(savePath, images)
        print("done.                  ", end="\r")
        # 최근 받은 파일을 JSON으로 저장하기
        json = {'skip': num-1, 'title': title}
        saveJsonFile(os.path.join(titlePath, "data.json"), json)
    print("[*] Download Complete")

def parseImages(driver):
    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")
    contents = []
    try:
        contents = bs.find("div", {"class": "view-content"}).find_all("img")
    except Exception as e:
        print(e)
    return contents



def getImageList(driver, url):
    driver.get(url)

    contents = parseImages(driver)
    if len(contents) == 0:
        retry_wait(7, "[이미지목록] ")
        contents = parseImages(driver)
        if len(contents) == 0:
            return getImageList(driver, url)

    images = []
    for content in contents:
        images.append(content["src"])
    return images