import os
import pathlib
import re
import shutil
import sys
import time
import urllib.request
import zipfile
from datetime import date
from multiprocessing import Pool, cpu_count
from os.path import basename

import requests
import tqdm
import wget
from bs4 import BeautifulSoup
from mshow.config import Config
from mshow.imageCompress import imagesCompress
from mshow.imageConverter import convertImages

CUSTOM_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'


def pathName(path):
  path = re.sub(r"NEW\t+", "", path)

  path = path.replace('\n', '')
  path = re.sub(r"\t.*$", "", path)
  path = path.replace(':', '').replace('?', '').replace(
      '/', '').replace('!', '').replace('\\', '')
  path = path.replace("「", " ").replace("」", '').replace(".", "")
  path = path.replace("<", "").replace(">", "")
  path = path.replace("\"", "")

  path = path.strip()
  return path


def imagesDownload(title, savePath, images, chapter, seed):
  title = pathName(title)
  pathlib.Path(savePath).mkdir(parents=True, exist_ok=True)
  target = []
  # c = Config()

  for i, img in enumerate(images):
    # img = re.sub(r"mangashow\d.me", c.getName(), img[0])
    target.append([img, savePath, i+1])

  pool = Pool(processes=cpu_count())
  try:
    # for tar in target:
    #     __downloadFromUrl(tar)
    for _ in tqdm.tqdm(pool.imap_unordered(__downloadFromUrl, target),
                       total=len(target), ncols=68, desc="    Download", leave=False):
      pass
  finally:
    pool.close()
    pool.join()

  print(" "*80, end="\r")
  # if int(seed) > 0:
  #   convertImages(savePath, chapter, seed)
  # imagesCompress(savePath)

  __zipFolder(savePath + "-" + pathName(title) + ".cbz", savePath)
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
    req = urllib.request.Request(
        url, headers={'User-Agent': CUSTOM_USER_AGENT})
    with open(outputPath, "wb") as f:
      with urllib.request.urlopen(req) as r:
        f.write(r.read())

    # urllib.request.urlretrieve(url, "D:/abc/image/local-filename.jpg")
    # requests.urllib3.disable_warnings()
    # s = requests.Session()
    # s.headers.update({'Connection': 'keep-alive',
    #                   'User-Agent': CUSTOM_USER_AGENT})
    # r = s.get(url, stream=True, verify=False)
    # with open(outputPath, 'wb') as f:
    #   for chunk in r.content(chunk_size=4096):
    #     f.write(chunk)
    #   f.close()
  except:
    return
