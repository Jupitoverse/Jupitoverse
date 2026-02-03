@echo off
setlocal enabledelayedexpansion

title SR Feedback System - First Time Setup (Ollama + Qwen Model)

cls

echo ================================================================================
echo         SR Feedback System - FIRST TIME SETUP
echo         (Downloads Ollama + Qwen2.5-Coder Model)
echo ================================================================================
echo %date% %time%
echo.
echo  This script will:
echo   1. Download and install Ollama (if not installed)
echo   2. Check/Install compatible Python (3.10-3.12)
echo   3. Download Qwen2.5-Coder 14B model (~15GB)
echo   4. Install Python dependencies
echo   5. Start the application
echo.
echo  NOTE: First time setup may take 20-60 minutes depending on internet speed
echo.
echo ================================================================================
echo.

REM ============================================
REM STEP 1: CHECK/INSTALL OLLAMA
REM ============================================
echo [1/6] Checking Ollama installation...
where ollama >nul 2>&1
if errorlevel 1 (
    echo      [INFO] Ollama not found. Downloading installer...
    echo.
    
    if not exist "%TEMP%\ollama_setup" mkdir "%TEMP%\ollama_setup"
    
    echo      Downloading Ollama from https://ollama.com/download/OllamaSetup.exe
    echo      Please wait...
    echo.
    
    powershell -Command "try { $ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri 'https://ollama.com/download/OllamaSetup.exe' -OutFile '%TEMP%\ollama_setup\OllamaSetup.exe' -UseBasicParsing; Write-Host '      [OK] Download complete'; exit 0 } catch { Write-Host '      [ERROR] Download failed: ' + $_.Exception.Message; exit 1 }"
    
    if errorlevel 1 (
        echo.
        echo      [ERROR] Failed to download Ollama!
        echo      Please download manually from: https://ollama.com/download
        echo.
        pause
        exit /b 1
    )
    
    echo.
    echo      [INFO] Running Ollama installer...
    echo      Please follow the installation prompts.
    echo.
    
    start /wait "" "%TEMP%\ollama_setup\OllamaSetup.exe"
    
    del /q "%TEMP%\ollama_setup\OllamaSetup.exe" >nul 2>&1
    rmdir "%TEMP%\ollama_setup" >nul 2>&1
    
    echo.
    echo      [INFO] Refreshing environment...
    
    where ollama >nul 2>&1
    if errorlevel 1 (
        echo.
        echo      [WARN] Ollama installed but not in PATH yet.
        echo      Please CLOSE this window and run this script again.
        echo.
        pause
        exit /b 1
    )
    
    echo      [OK] Ollama installed successfully!
) else (
    echo      [OK] Ollama is already installed
)
echo.

REM ============================================
REM STEP 2: CHECK/INSTALL PYTHON (3.10-3.12)
REM ============================================
echo [2/6] Checking Python installation...
echo      [INFO] Looking for Python 3.10-3.12 (required for numpy/pandas)
echo.
set PYTHON_CMD=
set NEED_PYTHON_INSTALL=0

REM Try py -3.12
for /f "tokens=*" %%v in ('py -3.12 --version 2^>^&1') do set PY_CHECK=%%v
echo !PY_CHECK! | findstr /C:"Python 3.12" >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py -3.12
    echo      [OK] Found Python 3.12
    goto :python_found
)

REM Try py -3.11
for /f "tokens=*" %%v in ('py -3.11 --version 2^>^&1') do set PY_CHECK=%%v
echo !PY_CHECK! | findstr /C:"Python 3.11" >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py -3.11
    echo      [OK] Found Python 3.11
    goto :python_found
)

REM Try py -3.10
for /f "tokens=*" %%v in ('py -3.10 --version 2^>^&1') do set PY_CHECK=%%v
echo !PY_CHECK! | findstr /C:"Python 3.10" >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py -3.10
    echo      [OK] Found Python 3.10
    goto :python_found
)

REM Try default py
for /f "tokens=*" %%v in ('py --version 2^>^&1') do set PY_CHECK=%%v
echo !PY_CHECK! | findstr /C:"Python 3.10 Python 3.11 Python 3.12" >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    echo      [OK] Found compatible Python
    goto :python_found
)

REM Try python command
for /f "tokens=*" %%v in ('python --version 2^>^&1') do set PY_CHECK=%%v
echo !PY_CHECK! | findstr /C:"Python 3.10" >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    echo      [OK] Found Python 3.10
    goto :python_found
)
echo !PY_CHECK! | findstr /C:"Python 3.11" >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    echo      [OK] Found Python 3.11
    goto :python_found
)
echo !PY_CHECK! | findstr /C:"Python 3.12" >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    echo      [OK] Found Python 3.12
    goto :python_found
)

REM No compatible Python found - need to install
echo      [WARN] No compatible Python (3.10-3.12) found
echo.
echo      ================================================================
echo       Python 3.11 Required - Auto-Install Available
echo      ================================================================
echo       numpy/pandas require Python 3.10, 3.11, or 3.12
echo       Python 3.13+ is not yet supported by these libraries
echo      ================================================================
echo.
echo      Would you like to download and install Python 3.11?
echo.

choice /C YN /M "      Download Python 3.11 now"
if errorlevel 2 goto :manual_python_install
if errorlevel 1 goto :auto_python_install

:auto_python_install
echo.
echo      [INFO] Downloading Python 3.11.9 installer...
echo      This may take a few minutes...
echo.

if not exist "%TEMP%\python_setup" mkdir "%TEMP%\python_setup"

powershell -Command "$ProgressPreference = 'SilentlyContinue'; try { Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile '%TEMP%\python_setup\python-3.11.9-amd64.exe' -UseBasicParsing; Write-Host '      [OK] Download complete'; exit 0 } catch { Write-Host '      [ERROR] Download failed'; exit 1 }"

if errorlevel 1 (
    echo.
    echo      [ERROR] Failed to download Python!
    echo      Please download manually from: https://python.org/downloads/release/python-3119/
    echo.
    pause
    exit /b 1
)

echo.
echo      [INFO] Running Python 3.11.9 installer...
echo.
echo      ================================================================
echo       IMPORTANT: In the installer, make sure to check:
echo       [x] "Add python.exe to PATH"
echo       Then click "Install Now"
echo      ================================================================
echo.

start /wait "" "%TEMP%\python_setup\python-3.11.9-amd64.exe" InstallAllUsers=0 PrependPath=1 Include_test=0

del /q "%TEMP%\python_setup\python-3.11.9-amd64.exe" >nul 2>&1
rmdir "%TEMP%\python_setup" >nul 2>&1

echo.
echo      ================================================================
echo       Python installation complete!
echo       Please CLOSE this window and run First_time.bat again.
echo       This is required to refresh the PATH environment.
echo      ================================================================
echo.
pause
exit /b 0

:manual_python_install
echo.
echo      [INFO] Please install Python 3.11 manually from:
echo             https://python.org/downloads/release/python-3119/
echo.
echo      Make sure to check "Add Python to PATH" during installation.
echo      Then run this script again.
echo.
pause
exit /b 1

:python_found
for /f "tokens=*" %%i in ('!PYTHON_CMD! --version 2^>^&1') do set PYTHON_VERSION=%%i
echo      [OK] !PYTHON_VERSION! - Compatible!
echo      [OK] Using command: !PYTHON_CMD!
echo.

REM ============================================
REM STEP 3: START OLLAMA SERVER
REM ============================================
echo [3/6] Starting Ollama server...
echo      This will open in a new window...
echo.

powershell -Command "try { Invoke-WebRequest -Uri 'http://localhost:11434/api/tags' -Method GET -TimeoutSec 2 -ErrorAction Stop | Out-Null; exit 0 } catch { exit 1 }" >nul 2>&1
if errorlevel 1 (
    echo      Starting Ollama in new window...
    start "Ollama Server" ollama serve
    echo      Waiting for Ollama to initialize...
    timeout /t 5 /nobreak >nul
    
    powershell -Command "try { Invoke-WebRequest -Uri 'http://localhost:11434/api/tags' -Method GET -TimeoutSec 5 -ErrorAction Stop | Out-Null; Write-Host '      [OK] Ollama server is running on port 11434'; exit 0 } catch { Write-Host '      [WARN] Ollama may still be starting...'; exit 1 }"
) else (
    echo      [OK] Ollama is already running
)
echo.

REM ============================================
REM STEP 4: DOWNLOAD QWEN2.5-CODER MODEL
REM ============================================
echo [4/6] Checking/Downloading Qwen2.5-Coder model...
echo.

ollama list | findstr /C:"qwen2.5-coder:14b-instruct-q8_0" >nul 2>&1
if errorlevel 1 (
    echo      [INFO] Qwen2.5-Coder model not found. Downloading...
    echo.
    echo      ================================================================
    echo       DOWNLOADING: qwen2.5-coder:14b-instruct-q8_0
    echo       Size: ~15GB - This may take 15-45 minutes
    echo       Please do NOT close this window!
    echo      ================================================================
    echo.
    
    ollama pull qwen2.5-coder:14b-instruct-q8_0
    
    if errorlevel 1 (
        echo.
        echo      [ERROR] Model download failed!
        echo      Please try running: ollama pull qwen2.5-coder:14b-instruct-q8_0
        echo.
        pause
        exit /b 1
    )
    
    echo.
    echo      [OK] Qwen2.5-Coder model downloaded successfully!
) else (
    echo      [OK] Qwen2.5-Coder model is already installed
)
echo.

REM ============================================
REM STEP 5: INSTALL PYTHON DEPENDENCIES
REM ============================================
echo [5/6] Installing/updating Python dependencies...
echo      This may take 1-2 minutes on first run...
echo.

!PYTHON_CMD! -m pip install --upgrade pip setuptools wheel >nul 2>&1

echo      Installing requirements.txt...
!PYTHON_CMD! -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo      [ERROR] Failed to install dependencies!
    echo      Try running manually: !PYTHON_CMD! -m pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

!PYTHON_CMD! -m pip install streamlit >nul 2>&1

echo      [OK] All dependencies installed
echo.

REM ============================================
REM STEP 6: VERIFY SETUP
REM ============================================
echo [6/6] Verifying setup...
echo.

where ollama >nul 2>&1
if errorlevel 1 (
    echo      [FAIL] Ollama not found
) else (
    echo      [OK] Ollama installed
)

ollama list | findstr /C:"qwen2.5-coder:14b-instruct-q8_0" >nul 2>&1
if errorlevel 1 (
    echo      [FAIL] Qwen2.5-Coder model not found
) else (
    echo      [OK] Qwen2.5-Coder model ready
)

!PYTHON_CMD! -c "import numpy; print('      [OK] numpy', numpy.__version__)" 2>nul
if errorlevel 1 (
    echo      [FAIL] numpy not working
)

!PYTHON_CMD! -c "import pandas; print('      [OK] pandas', pandas.__version__)" 2>nul
if errorlevel 1 (
    echo      [FAIL] pandas not working
)

echo.

REM ============================================
REM START FLASK APPLICATION
REM ============================================
echo ================================================================================
echo                        SETUP COMPLETE - STARTING APPLICATION
echo ================================================================================
echo.
echo  DEBUG INFO:
echo   - Python Command: !PYTHON_CMD!
echo   - Working Directory: %CD%
echo   - Script: sr_feedback_app.py
echo.
echo  SERVICES RUNNING:
echo   1. Ollama Server      - http://localhost:11434
echo   2. Flask Application  - http://localhost:5000
echo.
echo ================================================================================
echo  ACCESS PORTALS:
echo ================================================================================
echo.
echo  USER PORTAL:  http://localhost:5000
echo    - Search SRs and view AI-generated workarounds
echo    - Vote on workarounds (thumbs up/down) - NEW!
echo    - Provide feedback and corrections
echo    - Generate on-demand AI analysis
echo.
echo  ADMIN PORTAL: http://localhost:5000/admin
echo    - Username: admin ^| Password: admin123
echo    - Upload Excel files for batch processing
echo    - View system statistics
echo.
echo ================================================================================
echo  RAG FEATURES ENABLED:
echo ================================================================================
echo   [x] Historical AI Matching (20,399+ SRs)
echo   [x] User Feedback Learning (80%% similarity)
echo   [x] Java Backend Detection (11,795 classes)
echo   [x] LLM-Powered AI Workarounds (Qwen2.5-Coder)
echo   [x] On-Demand AI Generation
echo   [x] Comprehensive Troubleshooting Steps
echo.
echo ================================================================================
echo  IMPORTANT NOTES:
echo ================================================================================
echo   * Keep THIS window and OLLAMA window open
echo   * Using Qwen2.5-Coder 14B (8-bit) for ALL SR analysis
echo   * Batch processing: ~4-5 minutes per SR (40%% faster!)
echo   * Single SR regenerate: ~4-5 minutes
echo   * Press Ctrl+C to stop the Flask server
echo.
echo ================================================================================
echo.

echo Starting Flask with command: !PYTHON_CMD!
echo.

!PYTHON_CMD! sr_feedback_app.py

echo.
echo ================================================================================
echo                        APPLICATION STOPPED
echo ================================================================================
echo.
echo  To stop Ollama, close the "Ollama Server" window
echo.
echo %date% %time%
echo.
pause
endlocal
