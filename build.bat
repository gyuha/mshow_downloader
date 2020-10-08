CALL .\venv\Scripts\activate.bat
pyinstaller -y  --log-level=DEBUG --onefile --clean -F "manatoki.py" --version-file=file_version_info.txt -i icon.ico
copy phantomjs.exe dist
copy manatoki.ini dist
CALL .\venv\Scripts\deactivate.bat