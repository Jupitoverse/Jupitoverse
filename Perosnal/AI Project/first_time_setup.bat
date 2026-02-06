@echo off
title Data Annotation Platform - First Time Setup
echo.
echo ============================================
echo  Data Annotation Platform - First Time Setup
echo ============================================
echo.

cd /d "%~dp0"

echo Checking Python...
python --version 2>nul
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.11+ and add it to PATH.
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo.

set BACKEND=%~dp0V3\backend
if not exist "%BACKEND%\requirements.txt" (
    echo ERROR: V3\backend\requirements.txt not found.
    pause
    exit /b 1
)

echo Installing dependencies from V3\backend\requirements.txt...
echo.
cd /d "%BACKEND%"
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: pip install failed.
    pause
    exit /b 1
)

echo.
echo ============================================
echo  Setup complete.
echo  Run start.bat to launch the app.
echo  Open http://localhost:8000 in your browser.
echo ============================================
echo.
pause
