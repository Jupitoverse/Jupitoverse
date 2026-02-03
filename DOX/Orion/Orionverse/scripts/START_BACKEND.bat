@echo off
echo ====================================
echo Starting Orionverse Backend Server
echo ====================================
echo.
cd /d "%~dp0backend"
echo Backend directory: %CD%
echo.
echo Starting Flask server...
echo Keep this window OPEN!
echo.
python app.py
echo.
echo Backend stopped!
pause

