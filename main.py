from downloader.driver import driver_init, driver_close
from downloader.chapters import chapterListParser
from downloader.chapterParser import chapterImages

def downloadTitle(title):
    driver = driver_init()
    chaterList = chapterListParser(driver, bookTitle)
    chapterImages(driver, bookTitle, chaterList)
    driver_close(driver)

if __name__ == '__main__':
    bookTitle = input("[*] Please input book title: ")
    bookTitle = bookTitle.strip()

    downloadTitle(bookTitle)
    
