@echo off
setlocal

:: Get the directory of the CMD file
set "SCRIPT_DIR=%~dp0"

:: Run the Python script with the directory as an argument
python code\fund_timelapse.py %SCRIPT_DIR%

pause

endlocal