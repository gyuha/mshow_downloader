CALL .\venv\Scripts\activate.bat
pyinstaller -y -F "mangashowme.py" --version-file=file_version_info.txt -i icon.ico
copy chromedriver.exe dist
copy config.ini dist
CALL .\venv\Scripts\deactivate.bat