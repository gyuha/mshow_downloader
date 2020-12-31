CALL .\venv\Scripts\activate.bat
pyinstaller --windowed --clean -F "clipboard.py" --version-file=file_version_info.txt -i icon.ico
CALL .\venv\Scripts\deactivate.bat