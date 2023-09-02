@echo off

rem Build "Fansly Downloader NG.exe"
pyinstaller ^
    -n "Fansly Downloader NG" ^
    --onefile ^
    --console ^
    --noupx ^
    --icon=resources\fansly_ng.ico ^
    "%~dp0fansly_downloader_ng.py"
