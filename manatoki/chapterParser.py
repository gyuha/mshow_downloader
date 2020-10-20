import os
import pathlib
import shutil
import time

from bs4 import BeautifulSoup
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
    pathlib.Path(os.path.join("complete")).mkdir(parents=True, exist_ok=True)
    if os.path.exists(tar):
      shutil.rmtree(tar, ignore_errors=True)
    shutil.move(titlePath, tar)
    shutil.rmtree(titlePath, ignore_errors=True)

  print("[*] Download Complete")


def parseImages(driver):
  html = driver.find_elements_by_class_name("view-padding")[1]
  # html = driver.find_element_by_xpath("/html/body")
  # print(html.get_attribute("outerHTML"))
  div = html.get_attribute("outerHTML")
  bs = BeautifulSoup(div, "html.parser")

  images = bs.select('div > div > img')
  if (len(images) == 0):
    images = bs.select('div > div > p >img')

  for i in reversed(range(len(images))):
    if images[i].has_attr('style'):
      del images[i]

  source = driver.page_source

  chapter = 0
  seed = 0

  # 아래 문장이 없으면 로딩이 되지 않은 것임.
  if "뷰어로 보기" not in source or len(images) == 0:
    return [], chapter, seed, False

  img_list = []

  keys = images[0].attrs.keys()

  attr = ''

  for key in keys:
    if "data" in key:
      attr = key

  for img in images:
    img_list.append(img.get(attr))
    # print(img.get('src'))
    # url = img.search(r"\"(https.*g)\"").group(1)
    # print(url)
    # print(img)

  # try:
  #   cdnDomains = re.search(r'var\s+cdn_domains\s+=\s+(.*);', html).group(1)
  #   domains = json.loads(cdnDomains)
  # except Exception:
  #   return [], chapter, seed, False

  # urls1 = []
  # urls2 = []
  # try:
  #   strData = re.search(r'var\s+img_list\s+=\s+(.*);', html).group(1)
  #   urls1 = json.loads(strData)
  #   strData = re.search(r'var\s+img_list1\s+=\s+(.*);', html).group(1)
  #   urls2 = json.loads(strData)

  #   chapter = int(re.search(r'var\s+chapter\s+=\s+(.*);', html).group(1))
  #   seed = int(re.search(r'var\s+view_cnt\s+=\s+(.*);', html).group(1))
  # except Exception:
  #   return [], chapter, seed, False

  # max = len(urls1)
  # if len(urls1) < len(urls2):
  #   max = len(urls2)

  # for i in range(max):
  #   u = []
  #   t = domains[(chapter + 4 * i) % len(domains)]
  #   if (i < len(urls1)):
  #     urls1[i] = urls1[i].replace("cdntigermask.xyz", t)
  #     urls1[i] = urls1[i].replace("cdnmadmax.xyz", t)
  #     urls1[i] = urls1[i].replace("filecdn.xyz", t)
  #     u.append(urls1[i])
  #   if (i < len(urls2)):
  #     urls2[i] = urls2[i].replace("cdntigermask.xyz", t)
  #     urls2[i] = urls2[i].replace("cdnmadmax.xyz", t)
  #     urls2[i] = urls2[i].replace("filecdn.xyz", t)
  #     u.append(urls2[i])
  #   img_list.append(u)

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
        (By.CSS_SELECTOR, '.comic-navbar')))
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
