@echo off
REM ============================================================================
REM Install Required Python Packages
REM ============================================================================

echo.
echo ========================================================================
echo   Installing Required Packages
echo ========================================================================
echo.

REM Try py launcher first
where py >nul 2>&1
if %errorlevel% equ 0 (
    echo Using py launcher...
    py -m pip install mysql-connector-python psycopg2-binary pandas openpyxl pywin32
    goto :end
)

REM Try python in PATH
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo Using python...
    python -m pip install mysql-connector-python psycopg2-binary pandas openpyxl pywin32
    goto :end
)

echo ERROR: Python not found!
echo Please install Python first.
pause
exit /b 1

:end
echo.
echo ========================================================================
echo Installation completed!
echo ========================================================================
echo.
pause

