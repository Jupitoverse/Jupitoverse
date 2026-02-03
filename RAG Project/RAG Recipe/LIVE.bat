@echo off
title RAG Recipe - Server
pushd "%~dp0"

echo.
echo ========================================
echo   RAG Recipe - Starting on localhost
echo ========================================
echo.

set PYTHONPATH=%CD%

echo [1/2] Checking dependencies...
pip install -r requirements.txt -q 2>nul
if errorlevel 1 (
    echo       Running: pip install -r requirements.txt
    pip install -r requirements.txt
)

echo [2/2] Starting server at http://127.0.0.1:8000
echo.
echo   Once you see "Uvicorn running on http://127.0.0.1:8000"
echo   open in your browser:  http://127.0.0.1:8000
echo.
echo   Press Ctrl+C to stop the server.
echo ========================================
echo.

start "" "http://127.0.0.1:8000"

python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000

popd
pause
