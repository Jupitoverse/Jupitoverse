@echo off
title Orionverse Agent - Starting...
cls

echo ================================================================================
echo         ORIONVERSE AGENT - Combined Web + AI Application
echo ================================================================================
echo.

REM Check Python
where py >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.10-3.12
    pause
    exit /b 1
)

echo [INFO] Starting Orionverse Agent...
echo.
echo [STEP 1/2] Starting Backend Server (Port 5001)...

REM Start backend in a new window
start "Orionverse Backend" cmd /c "cd /d "%~dp0backend" && py -3.11 app.py"

REM Wait for backend to start
timeout /t 3 /nobreak >nul

echo [STEP 2/2] Starting Frontend Server (Port 8080)...

REM Start frontend in a new window
start "Orionverse Frontend" cmd /c "cd /d "%~dp0" && py -3.11 -m http.server 8080"

REM Wait for frontend to start
timeout /t 2 /nobreak >nul

echo.
echo ================================================================================
echo                      APPLICATION STARTED SUCCESSFULLY!
echo ================================================================================
echo.
echo  ACCESS POINTS:
echo  --------------
echo  Frontend:        http://localhost:8080
echo  Backend API:     http://localhost:5001
echo.
echo  FEATURES:
echo  ---------
echo  - Home Dashboard
echo  - Smart SR Assignment (AI-Powered)
echo  - Search Anything (32K+ SRs)
echo  - Bulk Handling (B1-B6)
echo  - Workarounds Database
echo.
echo ================================================================================
echo.

REM Open browser
echo Opening browser...
timeout /t 1 /nobreak >nul
start http://localhost:8080

echo.
echo Press any key to close this window (servers will keep running)...
pause >nul




