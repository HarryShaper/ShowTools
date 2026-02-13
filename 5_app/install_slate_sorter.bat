@echo off
setlocal

:: Directory where this installer lives
set TOOL_DIR=%~dp0

::Path to the main batch that runs the tool
set TARGET_BAT=%TOOL_DIR%run_slate_sorter.bat

:: SendTo folder for the current user
set SENDTO_DIR=%APPDATA%\Microsoft\Windows\SendTo

:: Name of the shortcut
set SHORTCUT_NAME=Slate Sorter.lnk

:: Create the shortcut using PowerShell
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
"$s=(New-Object -ComObject WScript.Shell).CreateShortcut('%SENDTO_DIR%\%SHORTCUT_NAME%'); ^
$s.TargetPath='%TARGET_BAT%'; ^
$s.WorkingDirectory='%TOOL_DIR%'; ^
$s.Save()"


:: Inform the user
echo.
echo Slate Sorter has been installed to Send To.
echo Right-click a folder ^> Send To ^> Slate Sorter
pause



