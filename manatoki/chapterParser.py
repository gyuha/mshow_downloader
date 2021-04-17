import os
import pathlib
import re
import shutil
import time

from bs4 import BeautifulSoup
from common import driver
from common.dataSave import loadJsonFile, saveJsonFile
from common.driver import reconnect, retry_wait
from common.imagesDownload import imagesDownload, pathName

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from manatoki.chapters import chapterListParser
from manatoki.config import Config

BASE_URL = '/comic/'
imageDownloadTryCount = 0


def saveFolderPath(titlePath, num):
    path = os.path.join(titlePath, "%03d" % (num,))
    return path


def comicsDownload(driver, mangaId, downloadFolder):
    # 만화책에서 이미지 목록을 가져 와서 다운로드 하기
    chaterList, public_type, tags, author, title = chapterListParser(
        driver, mangaId)
    global imageDownloadTryCount

    if len(chaterList) == 0:
        print("[Error] 이미지를 찾을 수 없습니다. 타이틀을 확인 해 주세요.")
        return

    titlePath = os.path.join(downloadFolder, pathName(title))

    pathlib.Path(titlePath).mkdir(parents=True, exist_ok=True)
    os.utime(pathlib.Path(titlePath), None)
    skip_num = 0
    saveData = loadJsonFile(os.path.join(titlePath, "data.json"))
    if saveData:
        skip_num = int(saveData["skip"])

    num = 1
    for d in chaterList:
        c = Config()
        url = d["href"]
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
        imagesDownload(d["title"], savePath, images, chapter, seed)

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

    # 완결인 책자를 별도로 저장해 준다.
    if public_type == "완결" or public_type == "단편":
        print("#"*80)
        print("#"*2 + " 완결: " + title)
        print("#"*80)
        title = pathName(title)
        tar = os.path.join("complete", title)
        pathlib.Path(os.path.join("complete")).mkdir(
            parents=True, exist_ok=True)
        if os.path.exists(tar):
            shutil.rmtree(tar, ignore_errors=True)
        shutil.move(titlePath, tar)
        shutil.rmtree(titlePath, ignore_errors=True)

    print("[*] Download Complete")


def parseImages(driver):
    time.sleep(0.5)
    view = driver.find_elements_by_class_name("view-padding")[1]

    imgs = view.find_elements_by_tag_name("img")

    for i in reversed(range(len(imgs))):
        if not imgs[i].is_displayed():
            # 보이지 않는 이미지는 제거
            del imgs[i]

    img_list = []

    # imageRe = re.compile("data-.*=\"(.*\.\w{3,4})\"")
    imageRe = re.compile(
        "data-.*=\"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)\"")
    for img in imgs:
        imgTag = img.get_attribute('outerHTML')
        if imageRe.search(imgTag) != None:
            img_list.append(imageRe.search(imgTag).group(1))

    print('📢[chapterParser.py:122]:', img_list)
    source = driver.page_source

    chapter = 0
    seed = 0

    # 아래 문장이 없으면 로딩이 되지 않은 것임.
    if "뷰어로 보기" not in source or len(img_list) == 0:
        return [], chapter, seed, False

    return img_list, chapter, seed, True


def getImageList(driver, url):
    global imageDownloadTryCount
    imageDownloadTryCount = imageDownloadTryCount + 1
    wait = WebDriverWait(driver, 30)
    try:
        driver.get(url)
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.comic-navbar')))
        time.sleep(0.5)
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
