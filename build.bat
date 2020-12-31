CALL .\venv\Scripts\activate.bat
:: pyinstaller --clean -w -F "manatoki.py" --version-file=file_version_info.txt -i icon.ico
pyinstaller --clean --log-level DEBUG --onefile --console  "manatoki.py"  --version-file=file_version_info.txt -i icon.ico
copy phantomjs.exe dist
copy chromedriver.exe dist
copy manatoki.ini dist
CALL .\venv\Scripts\deactivate.bat