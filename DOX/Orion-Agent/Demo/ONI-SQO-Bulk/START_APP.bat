@echo off
title ONI-SQO-Bulk Console
echo ============================================================
echo            ONI-SQO-Bulk Console - Startup
echo ============================================================
echo.

cd /d "%~dp0"

:: Check Python
where py >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

:: Start Backend
echo Starting Backend Server (Port 5003)...
start "Backend" cmd /k "cd backend && py -3.11 app.py"

:: Wait for backend to start
timeout /t 3 /nobreak >nul

:: Start Frontend
echo Starting Frontend Server (Port 8080)...
start "Frontend" cmd /k "py -3.11 -m http.server 8080"

echo.
echo ============================================================
echo    Servers Started Successfully!
echo ============================================================
echo.
echo    Frontend: http://localhost:8080
echo    Backend:  http://localhost:5003
echo.
echo    Press any key to open in browser...
pause >nul

start http://localhost:8080
