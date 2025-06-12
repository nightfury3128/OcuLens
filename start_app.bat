@echo off
echo Checking Python installation...
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Checking and installing required packages...
python -m pip install -r requirements.txt

echo Starting the application...
python main.py

pause
