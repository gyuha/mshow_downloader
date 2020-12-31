import os
import re
import urllib.parse
from collections import OrderedDict

from bs4 import BeautifulSoup
from common.dataSave import loadJsonFile
from common.driver import driver_close, driver_init, retry_wait
from common.imagesDownload import pathName
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from manatoki.config import Config

LIST_URL = "%s/bbs/page.php?hid=update&page=%d"

# 기존에 다운로드 받았던 id 목록


def downloadFiles(folderList):
  downloadList = []
  for downloaded in folderList:
    data = loadJsonFile(os.path.join("download", downloaded, "data.json"))
    if not data:
      continue
    if "id" in data:
      downloadList.append(data["id"])
  return downloadList


# 다운받은적 있는지 무식하게 찾는다
def existDownload(folerList, mangaId):
  for downloaded in folerList:
    data = loadJsonFile(os.path.join("download", downloaded, "data.json"))
    if not data:
      continue
    if "id" in data:
      if mangaId == data["id"]:
        return data["id"]
  return ""


def parseList(folderList, driver):
  downloadedList = downloadFiles(folderList)
  updateList = []
  try:
    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")

    subjects = bs.find(
        "div", {"class", "post-wrap"}).find_all("div", {"class", "post-info"})
    for subject in subjects:
      # mangaId = subject.find("a")['href']
      # mangaId = urllib.parse.unquote(mangaId)
      # mangaId = re.sub(r"^.*manga_id=", "", mangaId)
      # mangaId = mangaId.replace("+", " ")
      mangaId = subject.find("a")["rel"][0]
      # print(title)
      if mangaId == "":
        continue
      if mangaId in downloadedList:
        if mangaId not in updateList:
          updateList.append(mangaId)
  except Exception as e:
    print(e)
    return updateList
  print(updateList)
  return updateList

# 만화책에서 제목을 보고 업데이트 목록을 가져 옴


def filterDownloadedList(folerList, driver, page):
  c = Config()
  wait = WebDriverWait(driver, 30)
  print(LIST_URL % (c.getDomain(), page))
  driver.get(LIST_URL % (c.getDomain(), page))
  wait.until(EC.presence_of_element_located(
      (By.CSS_SELECTOR, '#thema_wrapper')))
  driver.execute_script("window.stop();")

  updateList = parseList(folerList, driver)

  # if len(updateList) == 0:
  #     retry_wait(7, "[업데이트목록] ")
  #     updateList = parseList(folerList, driver)
  #     if len(updateList) == 0:
  #         return filterDownloadedList(folerList, driver, page)

  return updateList


def getUpdateList(driver, updateSize=3):
  # 만화책 업데이트 목록 가져 오기
  folerList = os.listdir("download")
  updateList = []
  for i in range(1, updateSize + 1):
    print("[%d / %d] Download update list" % (i, updateSize), end="\r")
    downed = filterDownloadedList(folerList, driver, i)
    updateList = updateList + downed
  updateList = list(set(updateList))
  num = 0
  print("")
  print("Updated : %d" % len(updateList))
  for l in updateList:
    num = num + 1
    print("   %d. %s" % (num, l))
  return updateList


def checkAllDownload():
  folderList = os.listdir("download")
  updateList = []
  for downloaded in folderList:
    data = loadJsonFile(os.path.join("download", downloaded, "data.json"))
    if not data:
      continue
    if "id" in data:
      updateList.append(data["id"])
  return updateList
