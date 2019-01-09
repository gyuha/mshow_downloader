from bs4 import BeautifulSoup

base_url = "https://mangashow.me/bbs/page.php?hid=manga_detail&manga_name="

# 만화의 챕터 목록 가져 오기
def chapterListParser(driver, title):
    url = base_url + title
    driver.get(url)
    html = driver.page_source

    bs = BeautifulSoup(html, "html.parser")

    if not bs:
        print("Oppps........ Error Parser...")
        return []
    
    chapterList = bs.find("div", {"class": "chapter-list"})
    slots = chapterList.find_all("div", {"class": "slot"})
    data = []
    for slot in reversed(slots):
        text = slot.find("div", {"class":"title"}).getText().strip()
        data.append({
            "title": text,
            "wr_id": slot["data-wrid"]
        })

    return data
