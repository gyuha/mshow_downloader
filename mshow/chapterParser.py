import os
import pathlib
import time
import re
import json
from bs4 import BeautifulSoup
from mshow.chapters import chapterListParser
from mshow.imagesDownload import imagesDownload, pathName
from mshow.dataSave import saveJsonFile, loadJsonFile
from mshow.driver import retry_wait, reconnect

BASE_URL = 'https://mangashow2.me/bbs/board.php?bo_table=msm_manga&wr_id='


def saveFolderPath(titlePath, chapter, num):
    chapter = pathName(chapter)
    path = os.path.join(titlePath, "%03d" % (num,) + "-" + pathName(chapter))
    return path

# 만화책에서 이미지 목록을 가져 와서 다운로드 하기


def comicsDownload(driver, title, downloadFolder):
    chaterList, public_type, tags, author = chapterListParser(driver, title)

    if len(chaterList) == 0:
        print("[Error] 이미지를 찾을 수 없습니다. 타이틀을 확인 해 주세요.")
        return

    # 완결인 책자를 별도로 저장해 준다.
    if public_type == "완결":
        downloadFolder = os.path.join(downloadFolder, "[완결]")

    titlePath = os.path.join(downloadFolder, pathName(title))

    pathlib.Path(titlePath).mkdir(parents=True, exist_ok=True)
    skip_num = 0
    saveData = loadJsonFile(os.path.join(titlePath, "data.json"))
    if saveData:
        skip_num = int(saveData["skip"])

    num = 1
    for d in chaterList:
        url = BASE_URL + d["wr_id"]
        if skip_num >= num:
            print("[" + str(num) + "/" + str(len(chaterList)) +
                  "] 패스 : " + d["title"], end="\r")
            num = num + 1
            continue
        savePath = saveFolderPath(titlePath, d["title"], num)
        print(" "*80, end="\r")
        print("[" + str(num) + "/" + str(len(chaterList)) + "] 다운로드 : " + d["title"])
        num = num + 1
        if os.path.exists(savePath + ".zip"):
            print("  이미 압축한 파일 :" + d["title"])
            continue
        print("  Get image list by url..", end="\r")

        images, chapter, seed = getImageList(driver, url)
        print("  Download images..      ", end="\r")

        if len(images) == 0:
            print("  이미지를 찾을 수 없습니다. 패스")
            continue
        imagesDownload(savePath, images)

        # 최근 받은 파일을 JSON으로 저장하기
        json = {
            'author': author,
            'skip': num-1,
            'title': title,
            'public_type': public_type,
            'tags': tags
        }
        saveJsonFile(os.path.join(titlePath, "data.json"), json)
    print("[*] Download Complete")


def parseImages(driver):
    html = driver.page_source

    chapter = 0
    seed = 0

    # 아래 문장이 없으면 로딩이 되지 않은 것임.
    if "뷰어로 보기" not in html:
        return [], chapter, seed, False

    strData = re.search(r'var\s+img_list\s+=\s+(.*);', html).group(1)
    if not strData:
        return [], chapter, seed, False
    image_urls = json.loads(strData)

    if len(image_urls) == 0:
        return [], chapter, seed, False
    
    chapter = int(re.search(r'var\s+chapter\s+=\s+(.*);', html).group(1))
    seed = int(re.search(r'var\s+view_cnt\s+=\s+(.*);', html).group(1))
    
    # print(image_urls)
    # contents = []
    # try:
    #     contents = bs.find("div", {"class": "view-content"}).find_all("img")
    # except Exception as e:
    #     print(e)``
    return image_urls, chapter, seed, True


def getImageList(driver, url):
    try:
        driver.get(url)
    except Exception:
        reconnect(driver)
        return getImageList(driver, url)

    contents, chapter, seed, loading = parseImages(driver)

    # 로딩이 되지 않았으면... 다시 읽기
    if loading == False:
        retry_wait(7, "[이미지목록] ")
        contents, chapter, seed, loading = parseImages(driver)
        # 시간이 지났는데도 로딩이 되지 않으면..
        if loading == False:
            return getImageList(driver, url)

    # 로딩이 되었지만, 데이터가 없으면 패스
    if loading == True and len(contents) == 0:
        return []

    return contents, chapter, seed
