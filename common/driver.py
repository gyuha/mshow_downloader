import platform
import sys
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# browser = 'chrome'
browser = 'firefox'


def driver_init():
  # print("Chrome Driver loading...", end="\r")
  # capa = DesiredCapabilities.CHROME
  # capa["pageLoadStrategy"] = "none"

  # chrome_options.add_argument("--window-size=%s" % "800,600")

  if browser == 'chrome':
    driver_file = './geckodriver.exe'
    options = Options()
    # options.add_argument("--headless")
    # options.add_argument("--log-level=3")
    # options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(driver_file, chrome_options=options)
    # driver.implicitly_wait(5)
    return driver
  elif browser == 'firefox':
    driver_file = './geckodriver.exe'
    options = webdriver.FirefoxOptions()
    # options.set_headless()
    driver = webdriver.Firefox(
        executable_path=driver_file, firefox_options=options)
    # driver.implicitly_wait(5)
    return driver
  else:
    return


def driver_close(driver):
  driver.close()


def reconnect(driver):
  driver.close()
  driver = driver_init()
  return driver


def retry_wait(second, msg=""):
  for i in reversed(range(second)):
    print("%s데이터 읽기 오류... %d초후 다시 시도 합니다." % (msg, i+1), end="\r")
    time.sleep(1)
  # sys.stdout.write('\x1b[2K')
  print(" "*80, end="\r")
