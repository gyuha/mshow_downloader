import platform
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

def driver_init():
    print("[ ] Chrome Driver loading...", end="\r")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % "1920,1080")
    dirver_file = './chromedriver.exe'
    if platform.system() == 'Linux':
        dirver_file = './chromedriver'
    driver = webdriver.Chrome(executable_path=dirver_file,
                              chrome_options=chrome_options)
    driver.implicitly_wait(1)
    print("[*] Chrome Driver Starting...")

    return driver

def driver_close(driver):
    driver.close()