import shutil
from bs4 import BeautifulSoup
from mshow.chapters import base_url
from mshow.driver import driver_close, driver_init, reconnect
import multiprocessing
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from mshow.downloadList import downloadList
import os
from mshow.dataSave import loadJsonFile
from mshow.config import Config
import pathlib


def moveToCompleteFolder(name):
  print("====================================")
  print("완결: " + name)
  print("====================================")
  src = os.path.join("download", name)
  tar = os.path.join("complete", name)
  pathlib.Path(os.path.join("complete")).mkdir(parents=True, exist_ok=True)
  shutil.move(src, tar)
  shutil.rmtree(src, ignore_errors=True)


def checkComplete(driver, name, mangaId):
  config = Config()
  defaultIni = "config.ini"
  config.loadConfig(defaultIni)
  url = config.getDomain() + base_url + mangaId

  wait = WebDriverWait(driver, 30)
  try:
    driver.get(url)
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.at-footer')))
    driver.execute_script("window.stop();")
  except Exception:
    reconnect(driver)
    return checkComplete(driver, name, mangaId)

  html = driver.page_source
  bs = BeautifulSoup(html, "html.parser")

  try:
    publishType = bs.find("a", {"class": "publish_type"})
    type = publishType.getText().strip()
    if type == '완결':
      moveToCompleteFolder(name)
  except Exception as e:
    print(e)
    return


def downloadData(folderList):
  downloadList = []
  for downloaded in folderList:
    data = loadJsonFile(os.path.join("download", downloaded, "data.json"))
    if not data:
      continue
    if "id" in data:
      downloadList.append([downloaded, data["id"]])
  return downloadList


def start(driver):
  folerList = os.listdir("download")
  downloadedList = downloadData(folerList)
  for downloadedFile in downloadedList:
    print(downloadedFile)
    checkComplete(driver, downloadedFile[0], downloadedFile[1])


if __name__ == '__main__':
  multiprocessing.freeze_support()  # ! 꼭 바로 다음줄에 넣어 줘야 한다.
  driver = None
  driver = driver_init()

  start(driver)

  driver_close(driver)
