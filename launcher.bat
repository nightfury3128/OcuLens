@echo off
title iPhone Webcam Launcher
color 0A

echo.
echo ================================================
echo          iPhone Webcam Server Launcher
echo ================================================
echo.
echo Choose your preferred launch method:
echo.
echo 1. Auto Launch (Server + Browser + QR Code)
echo 2. Server Only (Manual browser access)
echo 3. System Tray App (Background service)
echo 4. Install Requirements
echo 5. Build Executable
echo 6. Exit
echo.

:choice
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto auto_launch
if "%choice%"=="2" goto server_only
if "%choice%"=="3" goto tray_app
if "%choice%"=="4" goto install_reqs
if "%choice%"=="5" goto build_exe
if "%choice%"=="6" goto exit
echo Invalid choice. Please try again.
goto choice

:auto_launch
echo.
echo Starting Auto Launch Mode...
echo - Server will start automatically
echo - Browser will open in 3 seconds
echo - QR code will be generated
echo - Desktop shortcut will be created
echo.
python main.py
goto end

:server_only
echo.
echo Starting Server Only Mode...
echo - Server will start
echo - Manual browser access required
echo.
python main.py
goto end

:tray_app
echo.
echo Starting System Tray App...
echo - Right-click the tray icon for options
echo - Server can be controlled from tray menu
echo.
python enhanced_tray_app.py
goto end

:install_reqs
echo.
echo Installing required packages...
pip install -r requirements.txt
echo.
echo Installation complete!
pause
goto choice

:build_exe
echo.
echo Building executable...
echo This may take several minutes...
echo.
pyinstaller --onefile --windowed --icon=icon.ico --name="iPhoneWebcam" main.py
echo.
echo Build complete! Check the 'dist' folder.
pause
goto choice

:exit
echo.
echo Goodbye!
goto end

:end
pause