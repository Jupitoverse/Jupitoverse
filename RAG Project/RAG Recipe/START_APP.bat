@echo off
pushd "%~dp0"
echo Starting RAG Recipe at http://127.0.0.1:8000
echo If the window closes or nothing loads, run in a terminal: python main.py
python main.py
popd
pause
