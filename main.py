from downloader.driver import driver_init, driver_close
from downloader.chapters import chapterListParser
from downloader.chapterParser import chapterImages

if __name__ == '__main__':
    bookTitle = input("[*] Please input book title: ")
    # bookTitle = "네가 우리들을 악마라 불렀을 적"
    bookTitle = bookTitle.strip()
    
    driver = driver_init()
    chaterList = chapterListParser(driver, bookTitle)
    chapterImages(driver, bookTitle, chaterList)
    driver_close(driver)
