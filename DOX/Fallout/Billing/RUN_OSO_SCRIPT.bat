@echo off
REM ============================================================================
REM Quick Run Script for OSO_Service_Activated.py
REM ============================================================================

echo.
echo ========================================================================
echo   OSO Service Activated - Data Sync Script
echo ========================================================================
echo.

REM Try py launcher first
where py >nul 2>&1
if %errorlevel% equ 0 (
    py OSO_Service_Activated.py %*
    goto :end
)

REM Try python in PATH
where python >nul 2>&1
if %errorlevel% equ 0 (
    python OSO_Service_Activated.py %*
    goto :end
)

REM Try common paths
if exist "C:\Python313\python.exe" (
    "C:\Python313\python.exe" OSO_Service_Activated.py %*
    goto :end
)

if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" OSO_Service_Activated.py %*
    goto :end
)

echo ERROR: Python not found!
pause
exit /b 1

:end
echo.
pause


