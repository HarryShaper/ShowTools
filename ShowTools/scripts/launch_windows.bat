@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%.."

cd /d "%ROOT_DIR%"

py "%ROOT_DIR%\showtools\ShowTools.py" %*

endlocal
pause