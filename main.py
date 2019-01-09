import sys, getopt

from mshow.driver import driver_init, driver_close
from mshow.chapters import chapterListParser
from mshow.chapterParser import chapterImages
from mshow.updateList import getUpdateList

def usage():
    print("python %s -u -s <PageSize>"%sys.argv[0])
    print("  -h, --help\t\tdisplay this help and exit")
    print("  -u, --update\t\tupdate downded comics")
    print("  -s, --size=SIZE\tupdate checked size(pages)")
    print("")
    print("If there is not any arguments, download by the comic title...")


def downloadTitle(bookTitle):
    driver = driver_init()
    chaterList = chapterListParser(driver, bookTitle)
    chapterImages(driver, bookTitle, chaterList)
    driver_close(driver)

def arguments():
    isUpdate = False
    updateSize = 3

    try:
        opts, _ = getopt.getopt(sys.argv[1:],"s:uh",["help","update","size="])
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
            updateSize = arg

    return isUpdate, updateSize

if __name__ == '__main__':
    isUpdate, updateSize = arguments()

    if isUpdate:
        # 업데이트 일 경우
        updatedList = getUpdateList(updateSize)
        num = 0
        for title in updatedList:
            num = num + 1
            print("############# DOWNLOAD [%d/%d] ###############"%(num, len(updatedList)))
            print(title)
            downloadTitle(title)
        print("Updated.....")
        num = 0
        for l in updatedList:
            num = num + 1
            print("   %d. %s"%(num, l))
    else:
        # 그냥 하나씩 다운로드
        bookTitle = input("[*] Please input book title: ")
        bookTitle = bookTitle.strip()

        downloadTitle(bookTitle)
