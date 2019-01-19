CALL .\venv\Scripts\activate.bat
pyinstaller -y -F "mangashowme.py"
copy chromedriver.exe dist
copy config.ini dist
CALL .\venv\Scripts\deactivate.bat