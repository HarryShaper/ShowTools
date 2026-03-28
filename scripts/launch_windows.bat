@echo on

cd /d "%~dp0.."

echo Running from:
cd

python -m showtools.ShowTools

echo.
echo Exit code: %errorlevel%
pause