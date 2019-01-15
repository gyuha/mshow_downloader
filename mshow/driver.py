import platform
import time
import sys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

def driver_init():
    print("Chrome Driver loading...", end="\r")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--window-size=%s" % "1920,1080")
    dirver_file = './chromedriver.exe'
    if platform.system() == 'Linux':
        dirver_file = './chromedriver'
    driver = webdriver.Chrome(executable_path=dirver_file,
                              chrome_options=chrome_options)
    driver.implicitly_wait(1)

    return driver

def driver_close(driver):
    driver.close()

def reconnect(driver):
    driver.close()
    driver = driver_init()
    return driver

def retry_wait(second, msg = ""):
    for i in reversed(range(second)):
        print("%s데이터 읽기 오류... %d초후 다시 시도 합니다."%(msg, i+1), end="\r")
        time.sleep(1)
    # sys.stdout.write('\x1b[2K')
    print(" "*80, end="\r")
