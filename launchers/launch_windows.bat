@echo off
setlocal

cd /d "%~dp0.."
python -m showtools.ShowTools "%~1"

endlocal