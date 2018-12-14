from bs4 import BeautifulSoup
from multiprocessing import Pool
from os.path import basename
import logging
import os
import pathlib
import requests
import shutil
import zipfile


CUSTOM_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36'

logging.basicConfig(filename='./log.txt', level=logging.ERROR)

def pathName(path):
    path = path.replace(':', '').replace('?', '').replace('/', '').replace('!', '').replace('\\', '')
    path = path.replace("「", " ").replace("」", '')
    path = path.strip()
    return path

def imagesDownload(titlePath, chapter, images):
    chapter = pathName(chapter)
    path = os.path.join(titlePath, pathName(chapter))

    zipFileName = path + ".zip"
    if os.path.exists(zipFileName):
        print("이미 압축함 : " + chapter)
        return
    print("Download : " + chapter)

    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    target = []
    i = 1
    for img in images:
        print(img)
        target.append([img, path, i])
        i = i + 1
    pool = Pool(processes=4)
    pool.map(__downloadFromUrl, target)

    __zipFolder(zipFileName, path)
    shutil.rmtree(path, ignore_errors=True)


def __zipFolder(filename, path):
    zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
    for f in os.listdir(path):
        zipf.write(os.path.join(path, f), basename(f))
    zipf.close()

def __downloadFromUrl(p):
    url = p[0]
    outputPath = p[1]
    num = p[2]

    name = "%03d" % (num,) + ".jpg"
    outputPath = os.path.join(outputPath, name)
    # print("Download : " + outputPath)

    try:
        s = requests.Session()
        s.headers.update({'User-Agent': CUSTOM_USER_AGENT})
        requests.urllib3.disable_warnings()
        r = s.get(url, stream=True, verify=False)
        with open(outputPath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
    except:
        return