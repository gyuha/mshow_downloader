import os
import requests
from bs4 import BeautifulSoup

LIST_PAGE = "https://mangashow.me/bbs/page.php?hid=manga_list&page=%d"
FILE_NAME = "comics.txt"
def parse(text):
    bs = BeautifulSoup(text, "html.parser")
    titles = bs.findAll("div", {"class":"post-list"})
    contents = ""
    for t in titles:
        title = t.find("div", {"class": "manga-subject"}).find("a").getText().strip()

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

        contents = contents + "%s\t%s\t%s\t%s\n"%(title, auth, tags, category)
    return contents


def getComicsList(pages):
    
    if os.path.exists(FILE_NAME):
        os.remove(FILE_NAME)

    with open(FILE_NAME, "a", encoding="utf8") as out:
            out.write("%s\t%s\t%s\t%s\n" %
                      ("제목", "작가", "태그", "분류"))

    for page in range(pages):
        print(LIST_PAGE%page, end="\r")
        r = requests.get(LIST_PAGE%page)
        content = parse(r.text)
        with open(FILE_NAME, "a", encoding="utf8") as out:
            out.write(content)
        # print(r.text)
        # break;
