import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from manatoki.config import Config
from bs4 import BeautifulSoup
from common.imagesDownload import pathName
from common.driver import retry_wait, reconnect

base_url = "/comic/"


def parseChaterList(driver):
  html = driver.page_source

  if "총 0화" in html:
    return [], False
  bs = BeautifulSoup(html, "html.parser")

  chapterList = []
  try:
    chapterList = bs.find(
        "div", {"class": "serial-list"}).find_all("a", {"class": "item-subject"}, limit=None)
  except Exception as e:
    print(e)
  # print(chapterList)
  # print(len(chapterList))
  return chapterList, True


def publishType(bs):
  publis_type = ""
  try:
    publis_type = bs.find("div", {"itemprop": "description"}).find_all(
        "div", {"class": "view-content"})[3].find("a").text.strip()
  except Exception:
    return ""
  return publis_type


def publishTags(bs):
  tags = []
  try:
    aTags = bs.find("div", {"itemprop": "description"}).find_all(
        "div", {"class": "view-content"})[2].find_all("a")
  except Exception:
    return []

  for tag in aTags:
    t = tag.text.strip()
    if len(t) > 0:
      tags.append(t)
  return tags


def publishAuthor(bs):
  author = ""
  try:
    author = bs.find("div", {"itemprop": "description"}).find_all(
        "div", {"class": "view-content"})[1].find("a").text.strip()
  except Exception:
    return ""
  return author


def publishTitle(bs):
  title = ""
  try:
    title = bs.find("div", {"itemprop": "description"}).find_all(
        "div", {"class": "view-content"})[0].text.strip()
  except Exception:
    return ""
  return title

# 만화의 챕터 목록 가져 오기


def chapterListParser(driver, mangaId):
  c = Config()
  url = c.getDomain() + base_url + mangaId
  publish_type = ""
  tags = []
  author = ""

  wait = WebDriverWait(driver, 10)
  try:
    driver.get(url)
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.control-sidebar-bg')))
    driver.execute_script("window.stop();")
  except Exception:
    reconnect(driver)
    return chapterListParser(driver, mangaId)

  chapterList = []
  valid = True
  chapterList, valid = parseChaterList(driver)
  if len(chapterList) == 0 and valid == True:
    retry_wait(6, "[도서 목록] ")
    chapterList, valid = parseChaterList(driver)
    if len(chapterList) == 0:
      return chapterListParser(driver, mangaId)

  if not valid:
    print("잘 못 된 URL입니다.")
    return [], publish_type, tags, author

  html = driver.page_source
  bs = BeautifulSoup(html, "html.parser")
  publish_type = publishType(bs)
  tags = publishTags(bs)
  author = publishAuthor(bs)
  title = publishTitle(bs)

  data = []
  for slot in reversed(chapterList):
    text = slot.getText().strip()
    text = pathName(text)
    data.append({
        "title": text,
        "href": slot["href"]
    })

  return data, publish_type, tags, author, title
