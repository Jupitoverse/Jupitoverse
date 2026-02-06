@echo off
title Data Annotation Platform
cd /d "%~dp0"

set BACKEND=%~dp0V3\backend
if not exist "%BACKEND%\app\main.py" (
    echo ERROR: V3\backend not found. Run first_time_setup.bat first.
    pause
    exit /b 1
)

echo Starting Data Annotation Platform...
echo Open http://localhost:8000 in your browser.
echo Press Ctrl+C to stop.
echo.

cd /d "%BACKEND%"
set PYTHONPATH=%BACKEND%
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
