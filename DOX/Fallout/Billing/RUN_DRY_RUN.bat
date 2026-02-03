@echo off
REM ============================================================================
REM Quick Dry Run - Test without sending email
REM ============================================================================

echo.
echo ========================================================================
echo   DRY RUN MODE - Testing without email
echo ========================================================================
echo.

REM Try py launcher first
where py >nul 2>&1
if %errorlevel% equ 0 (
    py Service_Activated.py --dry-run
    goto :end
)

REM Try python in PATH
where python >nul 2>&1
if %errorlevel% equ 0 (
    python Service_Activated.py --dry-run
    goto :end
)

REM Try common paths
if exist "C:\Python313\python.exe" (
    "C:\Python313\python.exe" Service_Activated.py --dry-run
    goto :end
)

if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" Service_Activated.py --dry-run
    goto :end
)

echo ERROR: Python not found!
pause
exit /b 1

:end
echo.
pause

