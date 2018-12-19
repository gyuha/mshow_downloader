import os
import pathlib

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
            print("패스 : [" + str(num) + "/" + str(len(data)) + "]" + d["title"] )
            num = num + 1
            continue
        savePath = saveFolderPath(titlePath, d["title"], num)
        print("다운로드 : [" + str(num) + "/" + str(len(data)) + "]" + d["title"])
        num = num + 1
        if os.path.exists(savePath + ".zip"):
            print("이미 압축한 파일 :" + d["title"])
            continue
        driver.get(url)
        images = getImageList(driver.page_source)
        imagesDownload(savePath, images)
    # print(data)
    data = {'skip': num-1}
    saveJsonFile(os.path.join(titlePath, "data.json"), data)
    print("[*] Download Complete")


def getImageList(html):
    bs = BeautifulSoup(html, "html.parser")
    contents = bs.find("div", {"class": "view-content"}).find_all("img")
    images = []
    for content in contents:
        images.append(content["src"])
    return images