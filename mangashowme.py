import sys, getopt
import multiprocessing

import os

from mshow.config import Config, DOWNLOAD_PATH
from mshow.driver import driver_init, driver_close
from mshow.chapterParser import comicsDownload
from mshow.updateList import getUpdateList
from mshow.downloadList import downloadList
from mshow.comicsList import getComicsList

def usage():
    print("python %s -u -s <PageSize>"%sys.argv[0])
    print("  -h, --help\t\tdisplay this help and exit")
    print("  -u, --update\t\tupdate downded comics")
    print("  -s, --size=SIZE\tupdate checked size(pages)")
    print("  -d, --download=FILE\tdownload by title list file..")
    print("  -c, --config=FILE\tselect config file..")
    print("  -l, --list=SIZE\tget comics list..")
    print("")
    print("If there is not any arguments, download by the comic title...")



# 외부 파라미터 받기
def arguments():
    isUpdate = False
    updateSize = 3
    downloadFile = ""
    listSize = 0

    try:
        opts, _ = getopt.getopt(sys.argv[1:],"c:s:d:l:uh",["help","update","config=","size=", "download=", "list="])
    except getopt.GetoptError as err:
        print(str(err))
        print("")
        usage()
        sys.exit(2)

    defaultIni = "config.ini"
    if os.path.exists(defaultIni):
        config = Config()
        config.loadConfig(defaultIni)

    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-u", "--update"):
            isUpdate = True
        elif opt in ("-s", "--size"):
            updateSize = int(arg)
        elif opt in ("-d", "--download"):
            downloadFile = arg
        elif opt in ("-l", "--list"):
            listSize = arg
        elif opt in ("-c", "--config"):
            config = Config()
            config.loadConfig(arg)

    return isUpdate, updateSize, downloadFile, listSize

# 한번에 여러개 받기
def multipleDownload(driver, downList):
    num = 0
    for title in downList:
        num = num + 1
        print("############# DOWNLOAD [%d/%d] ###############"%(num, len(downList)))
        print(title)
        config = Config()
        comicsDownload(driver, title, config.getDownloadPath())
    print("Downloaded.....")
    num = 0
    for title in downList:
        num = num + 1
        print("   %d. %s"%(num, title))

if __name__ == '__main__':
    multiprocessing.freeze_support()    #! 꼭 바로 다음줄에 넣어 줘야 한다.

    isUpdate, updateSize, downloadFile, listSize = arguments()

    if int(listSize) > 0:
        getComicsList(int(listSize))
        exit(1)

    driver = None

    if isUpdate:
        # 업데이트 일 경우
        driver = driver_init()
        updatedList = getUpdateList(driver, updateSize)
        multipleDownload(driver, updatedList)
    elif downloadFile != "":
        # 파일에서 다운로드 목록 확인
        driver = driver_init()
        downList = downloadList(downloadFile)
        multipleDownload(driver, downList)
    else:
        # 그냥 하나씩 다운로드
        bookTitle = input("[*] Please input book title: ")
        bookTitle = bookTitle.strip()
        driver = driver_init()
        config = Config()
        comicsDownload(driver, bookTitle, config.getDownloadPath())
    
    driver_close(driver)
