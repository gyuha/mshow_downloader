import getopt
import multiprocessing
import os
import sys

from common.downloadList import (count_file_lines_and_first_line, downloadList,
                                 save_update_list,
                                 saveListFile)
from common.driver import driver_close, driver_init
from manatoki.chapterParser import comicsDownload
from manatoki.config import Config
from manatoki.updateList import getUpdateList

# from manatoki.comicsList import getComicsList
# from manatoki.updateList import checkAllDownload, getUpdateList


def usage():
    print("python %s -u -s <PageSize>" % sys.argv[0])
    print("  -h, --help\t\tdisplay this help and exit")
    print("  -u, --update\t\tupdate downded comics")
    print("  -a, --all\t\tupdate all downded comics")
    print("  -s, --size=SIZE\tupdate checked size(pages)")
    print("  -d, --download=FILE\tdownload by title list file..")
    print("  -l, --list=SIZE\tget comics list..")
    print("")
    print("If there is not any arguments, download by the comic title...")


def arguments():
    # 외부 파라미터 받기
    isUpdate = False
    isUpdateAll = False
    updateSize = 3
    downloadFile = ""
    listSize = 0

    try:
        opts, _ = getopt.getopt(sys.argv[1:], "c:s:d:l:uh:ah", [
                                "help", "all", "update", "config=", "size=", "download=", "list="])
    except getopt.GetoptError as err:
        print(str(err))
        print("")
        usage()
        sys.exit(2)

    defaultIni = "manatoki.ini"
    if os.path.exists(defaultIni):
        config = Config()
        config.loadConfig(defaultIni)
    else:
        print("ERROR: Cant not find config.ini")
        exit()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-u", "--update"):
            isUpdate = True
        elif opt in ("-a", "--all"):
            isUpdateAll = True
        elif opt in ("-s", "--size"):
            updateSize = int(arg)
        elif opt in ("-d", "--download"):
            downloadFile = arg
        elif opt in ("-l", "--list"):
            listSize = arg

    return isUpdate, isUpdateAll, updateSize, downloadFile, listSize

# 한번에 여러개 받기


def multipleDownload(driver, listFileName=""):
    num = 0
    total_download = 0
    while(1):
        [count, id] = count_file_lines_and_first_line(listFileName)
        if count == 0:
            break
        total_download = total_download + 1
        print(
            "############# 다운로드 갯수 / 남은 갯수  [%d / %d] ###############" % (total_download, count))
        print("ID : %s" % (id))
        config = Config()
        comicsDownload(driver, id, config.getDownloadPath())
        saveListFile(listFileName, id)

    print("Done.....")


if __name__ == '__main__':
    multiprocessing.freeze_support()  # ! 꼭 바로 다음줄에 넣어 줘야 한다.

    isUpdate, isUpdateAll, updateSize, downloadFile, listSize = arguments()

    # if int(listSize) > 0:
    #   getComicsList(int(listSize))
    #   exit(1)

    driver = None
    config = Config()

    if isUpdate:
        # 업데이트 일 경우
        driver = driver_init()
        updatedList = getUpdateList(driver, updateSize)
        save_update_list(downloadFile, updatedList)
        multipleDownload(driver, downloadFile)
    elif isUpdateAll:
        driver = driver_init()
        # updatedList = checkAllDownload()
        # multipleDownload(driver, updatedList)
    elif downloadFile != "":
        # 파일에서 다운로드 목록 확인
        driver = driver_init()
        multipleDownload(driver, downloadFile)
    else:
        # 그냥 하나씩 다운로드
        print(config.getDomain() +
              "/comic/[xxxx]")
        mangaId = input("[*] 책 아이디 : ")
        # bookTitle = bookTitle.strip()
        driver = driver_init()
        comicsDownload(driver, mangaId, config.getDownloadPath())

    driver_close(driver)
