@echo off
REM ============================================================================
REM Quick Run Script for Service_Activated_Windows.py
REM ============================================================================

echo.
echo ========================================================================
echo   Service Activated - Billing Report Script
echo ========================================================================
echo.

REM Try different Python installations
echo Searching for Python...

REM Try py launcher first (most reliable on Windows)
where py >nul 2>&1
if %errorlevel% equ 0 (
    echo Found: py launcher
    echo Running script...
    py Service_Activated.py %*
    goto :end
)

REM Try python in PATH
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo Found: python in PATH
    echo Running script...
    python Service_Activated.py %*
    goto :end
)

REM Try common Python installation paths
if exist "C:\Python313\python.exe" (
    echo Found: C:\Python313\python.exe
    "C:\Python313\python.exe" Service_Activated.py %*
    goto :end
)

if exist "C:\Python312\python.exe" (
    echo Found: C:\Python312\python.exe
    "C:\Python312\python.exe" Service_Activated.py %*
    goto :end
)

if exist "C:\Python311\python.exe" (
    echo Found: C:\Python311\python.exe
    "C:\Python311\python.exe" Service_Activated.py %*
    goto :end
)

if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    echo Found: Python 3.13 in LocalAppData
    "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" Service_Activated.py %*
    goto :end
)

if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    echo Found: Python 3.12 in LocalAppData
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" Service_Activated.py %*
    goto :end
)

if exist "%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe" (
    echo Found: Microsoft Store Python
    "%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe" Service_Activated.py %*
    goto :end
)

REM If nothing found
echo.
echo ========================================================================
echo ERROR: Python not found!
echo ========================================================================
echo.
echo Please install Python from: https://www.python.org/downloads/
echo Or check if Python is installed by opening a new command prompt and typing:
echo   py --version
echo.
pause
exit /b 1

:end
echo.
echo ========================================================================
echo Script execution completed
echo ========================================================================
echo.
pause

