@echo off
title ONI-SQO-Bulk Console - Network Deployment
color 0A

echo ============================================================
echo       ONI-SQO-Bulk Console - Network Deployment
echo ============================================================
echo.

cd /d "%~dp0"

:: Get local IP
echo Detecting your IP address...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    for /f "tokens=1" %%b in ("%%a") do (
        set LOCAL_IP=%%b
        goto :found_ip
    )
)
:found_ip

echo.
echo ============================================================
echo    YOUR IP ADDRESS: %LOCAL_IP%
echo ============================================================
echo.

:: Check Python
where py >nul 2>&1
if %errorlevel% neq 0 (
    where python >nul 2>&1
    if %errorlevel% neq 0 (
        echo ERROR: Python not found!
        echo Please install Python 3.11+ from python.org
        pause
        exit /b 1
    )
    set PYTHON_CMD=python
) else (
    set PYTHON_CMD=py -3.11
)

echo [1/3] Checking firewall rules...
netsh advfirewall firewall show rule name="ONI-SQO-Bulk Backend" >nul 2>&1
if %errorlevel% neq 0 (
    echo      Adding firewall rule for Backend (Port 5003)...
    netsh advfirewall firewall add rule name="ONI-SQO-Bulk Backend" dir=in action=allow protocol=tcp localport=5003 >nul 2>&1
)
netsh advfirewall firewall show rule name="ONI-SQO-Bulk Frontend" >nul 2>&1
if %errorlevel% neq 0 (
    echo      Adding firewall rule for Frontend (Port 8080)...
    netsh advfirewall firewall add rule name="ONI-SQO-Bulk Frontend" dir=in action=allow protocol=tcp localport=8080 >nul 2>&1
)
echo      Firewall rules configured!

echo.
echo [2/3] Starting Backend Server (Port 5003)...
start "ONI-SQO Backend" cmd /k "cd backend && %PYTHON_CMD% app.py"

:: Wait for backend
timeout /t 3 /nobreak >nul

echo [3/3] Starting Frontend Server (Port 8080)...
start "ONI-SQO Frontend" cmd /k "%PYTHON_CMD% -m http.server 8080 --bind 0.0.0.0"

echo.
echo ============================================================
echo              SERVERS STARTED SUCCESSFULLY!
echo ============================================================
echo.
echo    ACCESS FROM THIS MACHINE:
echo      http://localhost:8080
echo.
echo    ACCESS FROM OTHER MACHINES (share this with team):
echo      http://%LOCAL_IP%:8080
echo.
echo    TABS AVAILABLE:
echo      - SQO Tab:          http://%LOCAL_IP%:8080#sqo
echo      - ONI Tab:          http://%LOCAL_IP%:8080#oni
echo      - Bulk Handling:    http://%LOCAL_IP%:8080#bulk-handling
echo.
echo ============================================================
echo    Press any key to open in browser...
echo ============================================================
pause >nul

start http://localhost:8080
