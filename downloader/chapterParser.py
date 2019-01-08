import os
import pathlib
import time

from bs4 import BeautifulSoup
from downloader.imagesDownload import imagesDownload, pathName
from downloader.dataSave import saveJsonFile, loadJsonFile

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

        images = []
        while len(images) == 0:
            images = getImageList(driver, url, driver.page_source)
            print("Download images..      ", end="\r")
        imagesDownload(savePath, images)
        print("done.                  ", end="\r")
        # 최근 받은 파일을 JSON으로 저장하기
        json = {'skip': num-1, 'title': title}
        saveJsonFile(os.path.join(titlePath, "data.json"), json)
    print("[*] Download Complete")


def getImageList(driver, url, html):
    driver.get(url)
    bs = BeautifulSoup(html, "html.parser")
    try:
        contents = bs.find("div", {"class": "view-content"}).find_all("img")
    except:
        for i in reversed(range(6)):
            print("데이터 읽기 오류... %d초후 다시 시도 합니다."%(i+1), end="\r")
            time.sleep(1)
        print("                                                      ", end="\r")
        return []

    images = []
    for content in contents:
        images.append(content["src"])
    return images