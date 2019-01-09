import time
from bs4 import BeautifulSoup
from mshow.driver import retry_wait

base_url = "https://mangashow.me/bbs/page.php?hid=manga_detail&manga_name="

def parseChaterList(driver):
    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")

    chapterList = []
    try:
        chapterList = bs.find("div", {"class": "chapter-list"}).find_all("div", {"class": "slot"})
    except Exception as e:
        print(e)
    return chapterList

# 만화의 챕터 목록 가져 오기
def chapterListParser(driver, title):
    url = base_url + title
    driver.get(url)

    chapterList = []
    chapterList = parseChaterList(driver)
    if len(chapterList) == 0:
        retry_wait(7)
        chapterList = parseChaterList(driver)
        if len(chapterList) == 0:
            return chapterListParser(driver, title)

    data = []
    for slot in reversed(chapterList):
        text = slot.find("div", {"class":"title"}).getText().strip()
        data.append({
            "title": text,
            "wr_id": slot["data-wrid"]
        })

    return data
