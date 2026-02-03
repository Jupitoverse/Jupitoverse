@echo off
echo ============================================
echo   Orionverse Network Backend Startup
echo ============================================
echo.

REM Get the current machine's IP address
echo [1/4] Getting your machine's IP address...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set IP=%%a
    goto :ip_found
)
:ip_found
echo     Your IP: %IP%
echo.

REM Check if firewall rule exists
echo [2/4] Checking Windows Firewall...
netsh advfirewall firewall show rule name="Flask Orionverse Backend 5001" >nul 2>&1
if errorlevel 1 (
    echo     Firewall rule not found. Attempting to create...
    echo     Note: This may require Administrator privileges
    netsh advfirewall firewall add rule name="Flask Orionverse Backend 5001" dir=in action=allow protocol=TCP localport=5001 >nul 2>&1
    if errorlevel 1 (
        echo     WARNING: Could not create firewall rule automatically
        echo     Please run this as Administrator or manually allow port 5001
    ) else (
        echo     ✓ Firewall rule created successfully
    )
) else (
    echo     ✓ Firewall rule already exists
)
echo.

REM Start the backend
echo [3/4] Starting Flask Backend...
echo     Backend will be accessible at:
echo     - Local:   http://127.0.0.1:5001
echo     - Network: http://%IP%:5001
echo.
echo [4/4] Launching backend server...
echo     Press CTRL+C to stop the server
echo ============================================
echo.

cd /d "%~dp0backend"
python app.py

pause





