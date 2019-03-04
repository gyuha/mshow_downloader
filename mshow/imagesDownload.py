from bs4 import BeautifulSoup
from mshow.imageConverter import convertImages
from multiprocessing import Pool, cpu_count
from os.path import basename
from mshow.config import Config
import os
import pathlib
import re
import requests
import shutil
import sys
import time
import tqdm
import zipfile

CUSTOM_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36'

def pathName(path):
    path = re.sub(r"NEW\t+", '', path)
    path = path.replace(':', '').replace('?', '').replace('/', '').replace('!', '').replace('\\', '')
    path = path.replace("「", " ").replace("」", '').replace(".", "").replace('\t', ' ')
    path = path.replace("<", "").replace(">", "")
    path = path.strip()
    return path

def imagesDownload(savePath, images, chapter, seed):
    pathlib.Path(savePath).mkdir(parents=True, exist_ok=True)
    target = []
    i = 1
    c = Config()

    for img in images:
        img = re.sub(r"mangashow\d.me", c.getName(), img)
        target.append([img, savePath, i])
        i = i + 1
    
    pool = Pool(processes=cpu_count())
    try:
        for _ in tqdm.tqdm(pool.imap_unordered(__downloadFromUrl, target), 
            total=len(target), ncols=68, desc="    Download", leave=False):
            pass
        # pool.map(__downloadFromUrl, target)
    finally:
        pool.close()
        pool.join()

    print(" "*80, end="\r")
    if seed > 0:
        convertImages(savePath, chapter, seed)

    __zipFolder(savePath + ".zip", savePath)
    shutil.rmtree(savePath, ignore_errors=True)


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

    try:
        requests.urllib3.disable_warnings()
        s = requests.Session()
        s.headers.update({'User-Agent': CUSTOM_USER_AGENT})
        r = s.get(url, stream=True, verify=False)
        with open(outputPath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
    except:
        return
    