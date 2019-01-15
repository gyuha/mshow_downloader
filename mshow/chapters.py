import time
from bs4 import BeautifulSoup
from mshow.driver import retry_wait

base_url = "https://mangashow.me/bbs/page.php?hid=manga_detail&manga_name="

def parseChaterList(driver):
    html = driver.page_source

    if "총 0화" in html:
        return [], False
    bs = BeautifulSoup(html, "html.parser")

    chapterList = []
    try:
        chapterList = bs.find("div", {"class": "chapter-list"}).find_all("div", {"class": "slot"})
    except Exception as e:
        print(e)

    return chapterList, True


def publishType(bs):
    publis_type = ""
    try:
         publis_type = bs.find("a", {"class": "publish_type"}).text.strip()
    except Exception:
        return ""
    return publis_type

def publishTags(bs):
    tags = []
    try:
        aTags = bs.find_all("a", {"class": "tag"})
    except Exception:
        return []
    
    for tag in aTags:
        t = tag.text.strip()
        if len(t) > 0:
            tags.append(t)
    return tags

# 만화의 챕터 목록 가져 오기
def chapterListParser(driver, title):
    url = base_url + title
    driver.get(url)
    publish_type = ""
    tags = []

    chapterList = []
    valid = True
    chapterList, valid = parseChaterList(driver)
    if len(chapterList) == 0 and valid == True:
        retry_wait(7, "[도서 목록] ")
        chapterList, valid = parseChaterList(driver)
        if len(chapterList) == 0:
            return chapterListParser(driver, title)

    if not valid:
        print("잘 못 된 URL입니다.")
        return []

    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")
    publish_type = publishType(bs)
    tags = publishTags(bs)

    data = []
    for slot in reversed(chapterList):
        text = slot.find("div", {"class":"title"}).getText().strip()
        data.append({
            "title": text,
            "wr_id": slot["data-wrid"]
        })

    return data, publish_type, tags
