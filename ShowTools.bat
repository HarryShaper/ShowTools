@echo off
setlocal

set "APP_DIR=%~dp0"
cd /d "%APP_DIR%"

py "%APP_DIR%ShowTools.py" %*

endlocal
pause