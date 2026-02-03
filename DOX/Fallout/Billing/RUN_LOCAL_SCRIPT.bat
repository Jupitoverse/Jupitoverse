@echo off
REM ============================================================================
REM RUN_LOCAL_SCRIPT.bat - Run OSO_Service_Activated_local.py
REM ============================================================================
REM
REM This batch file runs the simplified local version of the script.
REM No WRITE DB connection, just fetch data and email report.
REM
REM ============================================================================

echo.
echo ================================================================================
echo   OSO Service Activated - Local Script Runner
echo ================================================================================
echo.

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo Current directory: %CD%
echo.

REM Check if Python script exists
if not exist "OSO_Service_Activated_local.py" (
    echo [ERROR] Script not found: OSO_Service_Activated_local.py
    echo Please ensure the script is in the same directory as this batch file.
    echo.
    pause
    exit /b 1
)

echo [OK] Found script: OSO_Service_Activated_local.py
echo.

REM Try to find Python executable
set "PYTHON_EXE="

REM Method 1: Check if python is in PATH
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PYTHON_EXE=python"
    echo [OK] Found Python in PATH
    goto :run_script
)

REM Method 2: Check if python3 is in PATH
where python3 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PYTHON_EXE=python3"
    echo [OK] Found Python3 in PATH
    goto :run_script
)

REM Method 3: Common installation paths
set "COMMON_PATHS=C:\Python39\python.exe;C:\Python310\python.exe;C:\Python311\python.exe;C:\Python312\python.exe;C:\Program Files\Python39\python.exe;C:\Program Files\Python310\python.exe;C:\Program Files\Python311\python.exe;C:\Program Files\Python312\python.exe;%LOCALAPPDATA%\Programs\Python\Python39\python.exe;%LOCALAPPDATA%\Programs\Python\Python310\python.exe;%LOCALAPPDATA%\Programs\Python\Python311\python.exe;%LOCALAPPDATA%\Programs\Python\Python312\python.exe"

for %%p in ("%COMMON_PATHS:;=" "%") do (
    if exist %%p (
        set "PYTHON_EXE=%%~p"
        echo [OK] Found Python at: %%~p
        goto :run_script
    )
)

REM If still not found, show error
echo [ERROR] Python not found!
echo.
echo Please ensure Python 3.x is installed.
echo.
echo Download from: https://www.python.org/downloads/
echo.
pause
exit /b 1

:run_script
echo.
echo ================================================================================
echo   Running Script...
echo ================================================================================
echo.
echo Python: %PYTHON_EXE%
echo Script: OSO_Service_Activated_local.py
echo.

REM Run the Python script
"%PYTHON_EXE%" OSO_Service_Activated_local.py

REM Check exit code
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================================================
    echo   Script completed successfully!
    echo ================================================================================
) else (
    echo.
    echo ================================================================================
    echo   Script failed with exit code: %ERRORLEVEL%
    echo ================================================================================
)

echo.
pause









