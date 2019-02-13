import os
import requests

from bs4 import BeautifulSoup
from urllib.parse import quote
from mshow.config import Config

LIST_PAGE = "%s/bbs/page.php?hid=manga_list&page=%d"
FILE_NAME = "comics.txt"
def parse(text):
    bs = BeautifulSoup(text, "html.parser")
    titles = bs.findAll("div", {"class":"post-list"})
    contents = ""
    for t in titles:
        title = t.find("div", {"class": "manga-subject"}).find("a").getText().strip()
        if len(title) == 0:
            continue
        link = ""
        linkA = t.find("a", {"class": "ellipsis"})
        if linkA is not None:
            link = "\"%s/bbs/page.php?hid=manga_detail&manga_name=" + quote(title) + "\""%(DOMAIN)
        img = ""
        imgDiv = t.find("div", {"class": "img-wrap-back"})
        if imgDiv is not None:
            img = imgDiv.attrs["style"]
            img = img.replace("background-image:url(", "")
            img = img[:-1]

        authDiv = t.find("div", {"class": "author"})
        auth = ""
        if authDiv is not None:
            auth = authDiv.getText().strip()

        category = ""
        cateDiv = t.find("div", {"class": "publish-type"})
        if cateDiv is not None:
            category = cateDiv.getText().strip()

        tags = ""
        tagsDiv = t.find("div", {"class": "tags"})
        if tagsDiv is not None:
            tags = tagsDiv.getText().strip()

        contents = contents + "%s\t%s\t%s\t%s\t%s\t%s\n"%(title, auth, tags, category, link, img)
    return contents


def getComicsList(pages):
    
    if os.path.exists(FILE_NAME):
        os.remove(FILE_NAME)

    with open(FILE_NAME, "a", encoding="utf8") as out:
            out.write("%s\t%s\t%s\t%s\t%s\t%s\n" %
                      ("제목", "작가", "태그", "분류", "링크","이미지"))

    for page in range(pages):
        c = Config()
        url = LIST_PAGE%(c.getDomain(), page)
        print(url, end="\r")
        r = requests.get(url)
        content = parse(r.text)
        with open(FILE_NAME, "a", encoding="utf8") as out:
            out.write(content)
        # print(r.text)
        # break;
