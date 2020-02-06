from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from mshow.chapters import chapterListParser
from mshow.config import Config
from mshow.dataSave import saveJsonFile, loadJsonFile
from mshow.driver import retry_wait, reconnect
from mshow.imagesDownload import imagesDownload, pathName
import json
import os
import pathlib
import re
import time

BASE_URL = '/bbs/board.php?bo_table=manga&wr_id='
imageDownloadTryCount = 0


def saveFolderPath(titlePath, num):
    path = os.path.join(titlePath, "%03d" % (num,))
    return path


# 만화책에서 이미지 목록을 가져 와서 다운로드 하기
def comicsDownload(driver, mangaId, downloadFolder):
    chaterList, public_type, tags, author, title = chapterListParser(
        driver, mangaId)
    global imageDownloadTryCount

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
        c = Config()
        url = c.getDomain() + BASE_URL + d["wr_id"]
        if skip_num >= num:
            print("[" + str(num) + "/" + str(len(chaterList)) +
                  "] 패스 : " + d["title"], end="\r")
            num = num + 1
            continue
        savePath = saveFolderPath(titlePath, num)
        print(" "*80, end="\r")
        print("[" + str(num) + "/" + str(len(chaterList)) + "] 다운로드 : " + d["title"])
        num = num + 1
        if os.path.exists(savePath + "." + c.getFileExtension()) or os.path.exists(savePath + ".zip"):
            print("  이미 압축한 파일 :" + d["title"])
            continue
        print("  Get image list by url..", end="\r")

        imageDownloadTryCount = 0
        images, chapter, seed = getImageList(driver, url)
        print("  Download images..      ", end="\r")

        if len(images) == 0:
            print("  이미지를 찾을 수 없습니다. 패스")
            continue
        imagesDownload(title, savePath, images, chapter, seed)

        # 최근 받은 파일을 JSON으로 저장하기
        json = {
            'author': author,
            'skip': num-1,
            'title': title,
            'public_type': public_type,
            'tags': tags,
            'id': mangaId
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

    img_list = []
    urls1 = []
    urls2 = []
    try:
        strData = re.search(r'var\s+img_list\s+=\s+(.*);', html).group(1)
        urls1 = json.loads(strData)
        strData = re.search(r'var\s+img_list1\s+=\s+(.*);', html).group(1)
        urls2 = json.loads(strData)
    except Exception:
        return [], chapter, seed, False

    max = len(urls1)
    if len(urls1) < len(urls2):
        max = len(urls2)

    for i in range(max):
        u = []
        if (i < len(urls1)):
            u.append(urls1[i])
        if (i < len(urls2)):
            u.append(urls2[i])
        img_list.append(u)

    chapter = int(re.search(r'var\s+chapter\s+=\s+(.*);', html).group(1))
    seed = int(re.search(r'var\s+view_cnt\s+=\s+(.*);', html).group(1))

    # print(image_urls)
    # contents = []
    # try:
    #     contents = bs.find("div", {"class": "view-content"}).find_all("img")
    # except Exception as e:
    #     print(e)``
    return img_list, chapter, seed, True


def getImageList(driver, url):
    global imageDownloadTryCount
    imageDownloadTryCount = imageDownloadTryCount + 1
    wait = WebDriverWait(driver, 30)
    try:
        driver.get(url)
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.scroll-viewer')))
        time.sleep(1)
        driver.execute_script("window.stop();")
    except Exception:
        # reconnect(driver)
        print('사이트 읽기 오류')
        if imageDownloadTryCount > 2:
            return [], 0, 0
        return getImageList(driver, url)

    contents, chapter, seed, loading = parseImages(driver)

    # 로딩이 되지 않았으면... 다시 읽기
    if loading == False:
        if imageDownloadTryCount > 2:
            return [], 0, 0
        retry_wait(7, "[이미지목록] ")
        contents, chapter, seed, loading = parseImages(driver)
        # 시간이 지났는데도 로딩이 되지 않으면..
        if loading == False:
            return getImageList(driver, url)

    # 로딩이 되었지만, 데이터가 없으면 패스
    if loading == True and len(contents) == 0:
        return [], 0, 0

    return contents, chapter, seed
