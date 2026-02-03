@echo off
pushd "%~dp0"
set PYTHONPATH=%CD%
echo RAG Recipe - Server will start at http://127.0.0.1:8000
echo.
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
popd
pause
