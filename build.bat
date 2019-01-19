pyinstaller -y -F "main.py"
copy chromedriver.exe ./dist
copy config.ini ./dist
