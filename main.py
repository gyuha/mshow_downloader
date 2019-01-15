import sys, getopt
import multiprocessing
import configparser
import os

from mshow.driver import driver_init, driver_close
from mshow.chapterParser import comicsDownload
from mshow.updateList import getUpdateList
from mshow.downloadList import downloadList

DOWNLOAD_FOLDER = "download"

def usage():
    print("python %s -u -s <PageSize>"%sys.argv[0])
    print("  -h, --help\t\tdisplay this help and exit")
    print("  -u, --update\t\tupdate downded comics")
    print("  -s, --size=SIZE\tupdate checked size(pages)")
    print("  -d, --download=FILE\tdownload by title list file..")
    print("  -c, --config=FILE\tselect config file..")
    print("")
    print("If there is not any arguments, download by the comic title...")

# config 파일 읽기
def readConfig(path):
    if os.path.exists(path):
        return ""

    downloadPath = ""
    config = configparser.ConfigParser()
    config.read(path)
    downloadPath = config["DEFAULT"]["path"]

    return downloadPath


# 외부 파라미터 받기
def arguments():
    isUpdate = False
    updateSize = 3
    global DOWNLOAD_FOLDER

    try:
        opts, _ = getopt.getopt(sys.argv[1:],"s:d:uh",["help","update","size=", "download="])
    except getopt.GetoptError as err:
        print(str(err))
        print("")
        usage()
        sys.exit(2)
    
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
        elif opt in ("-c", "--config"):
            DOWNLOAD_FOLDER = readConfig(arg)

    return isUpdate, updateSize, downloadFile

# 한번에 여러개 받기
def multipleDownload(driver, downList):
    num = 0
    for title in downList:
        num = num + 1
        print("############# DOWNLOAD [%d/%d] ###############"%(num, len(downList)))
        print(title)
        comicsDownload(driver, title, DOWNLOAD_FOLDER)
    print("Downloaded.....")
    num = 0
    for title in downList:
        num = num + 1
        print("   %d. %s"%(num, title))

if __name__ == '__main__':
    multiprocessing.freeze_support()    #! 꼭 바로 다음줄에 넣어 줘야 한다.

    isUpdate, updateSize, downloadFile = arguments()

    driver = driver_init()

    if isUpdate:
        # 업데이트 일 경우
        updatedList = getUpdateList(driver, updateSize)
        multipleDownload(driver, updatedList)
    elif downloadFile != "":
        # 파일에서 다운로드 목록 확인
        downList = downloadList(downloadFile)
        multipleDownload(driver, downList)
    else:
        # 그냥 하나씩 다운로드
        bookTitle = input("[*] Please input book title: ")
        bookTitle = bookTitle.strip()

        comicsDownload(driver, bookTitle, DOWNLOAD_FOLDER)
    
    driver_close(driver)
