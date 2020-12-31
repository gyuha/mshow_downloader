CALL .\venv\Scripts\activate.bat
pyinstaller -y --clean -F "manatoki.py" --version-file=file_version_info.txt -i icon.ico
pyinstaller -y --clean -F "clipboard.py" --version-file=file_version_info.txt -i icon.ico
copy phantomjs.exe dist
copy chromedriver.exe dist
copy manatoki.ini dist
CALL .\venv\Scripts\deactivate.bat