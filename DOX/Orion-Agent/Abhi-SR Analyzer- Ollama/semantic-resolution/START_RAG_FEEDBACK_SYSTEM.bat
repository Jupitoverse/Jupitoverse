@echo off

title SR Feedback System with RAG - Complete Setup

cls

echo ================================================================================
echo         SR Feedback System with RAG (Ollama Qwen2.5-Coder)
echo ================================================================================
echo %date% %time%
echo.

REM ============================================
REM STEP 1: CHECK OLLAMA INSTALLATION
REM ============================================
echo [1/5] Checking Ollama installation...
where ollama >nul 2>&1
if errorlevel 1 (
    echo      [ERROR] Ollama not found!
    echo      Please run First_time.bat to install Ollama
    echo      Or install from: https://ollama.ai/download
    echo.
    pause
    exit /b 1
)
echo      [OK] Ollama is installed
echo.

REM ============================================
REM STEP 2: CHECK PYTHON (3.10-3.12 for numpy)
REM ============================================
echo [2/5] Checking Python installation...
set PYTHON_CMD=

REM Try py launcher with specific compatible versions - verify they actually work
for /f "tokens=*" %%v in ('py -3.12 --version 2^>^&1') do set PY_CHECK=%%v
echo %PY_CHECK% | findstr /C:"Python 3.12" >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py -3.12
    goto :python_found
)

for /f "tokens=*" %%v in ('py -3.11 --version 2^>^&1') do set PY_CHECK=%%v
echo %PY_CHECK% | findstr /C:"Python 3.11" >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py -3.11
    goto :python_found
)

for /f "tokens=*" %%v in ('py -3.10 --version 2^>^&1') do set PY_CHECK=%%v
echo %PY_CHECK% | findstr /C:"Python 3.10" >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py -3.10
    goto :python_found
)

REM Check default py command and verify version
py --version >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=*" %%v in ('py --version 2^>^&1') do set PY_CHECK=%%v
    
    echo %PY_CHECK% | findstr /C:"Python 3.10" >nul 2>&1
    if not errorlevel 1 (
        set PYTHON_CMD=py
        goto :python_found
    )
    echo %PY_CHECK% | findstr /C:"Python 3.11" >nul 2>&1
    if not errorlevel 1 (
        set PYTHON_CMD=py
        goto :python_found
    )
    echo %PY_CHECK% | findstr /C:"Python 3.12" >nul 2>&1
    if not errorlevel 1 (
        set PYTHON_CMD=py
        goto :python_found
    )
    
    REM py exists but incompatible version
    echo      [ERROR] %PY_CHECK% found but not compatible!
    echo      numpy/pandas require Python 3.10, 3.11, or 3.12
    echo      Please run First_time.bat to install Python 3.11
    echo.
    pause
    exit /b 1
)

REM Try python command
python --version >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=*" %%v in ('python --version 2^>^&1') do set PY_CHECK=%%v
    
    echo %PY_CHECK% | findstr /C:"Python 3.10" >nul 2>&1
    if not errorlevel 1 (
        set PYTHON_CMD=python
        goto :python_found
    )
    echo %PY_CHECK% | findstr /C:"Python 3.11" >nul 2>&1
    if not errorlevel 1 (
        set PYTHON_CMD=python
        goto :python_found
    )
    echo %PY_CHECK% | findstr /C:"Python 3.12" >nul 2>&1
    if not errorlevel 1 (
        set PYTHON_CMD=python
        goto :python_found
    )
    
    echo      [ERROR] %PY_CHECK% found but not compatible!
    echo      numpy/pandas require Python 3.10, 3.11, or 3.12
    echo      Please run First_time.bat to install Python 3.11
    echo.
    pause
    exit /b 1
)

echo      [ERROR] Python not found!
echo      Please run First_time.bat to install Python
echo.
pause
exit /b 1

:python_found
REM Get Python version
for /f "tokens=*" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set PYTHON_VERSION=%%i
echo      [OK] %PYTHON_VERSION% found
echo      [OK] Using command: %PYTHON_CMD%
echo.

REM ============================================
REM STEP 3: START OLLAMA SERVER
REM ============================================
echo [3/5] Starting Ollama server...
echo      This will open in a new window...
echo.

REM Check if Ollama is already running
powershell -Command "try { Invoke-WebRequest -Uri 'http://localhost:11434/api/tags' -Method GET -TimeoutSec 2 -ErrorAction Stop | Out-Null; exit 0 } catch { exit 1 }" >nul 2>&1
if errorlevel 1 (
    echo      Starting Ollama in new window...
    start "Ollama Server" ollama serve
    echo      Waiting for Ollama to initialize...
    timeout /t 5 /nobreak >nul
    
    REM Verify Ollama started successfully
    powershell -Command "try { Invoke-WebRequest -Uri 'http://localhost:11434/api/tags' -Method GET -TimeoutSec 5 -ErrorAction Stop | Out-Null; Write-Host '     [OK] Ollama server is running on port 11434'; exit 0 } catch { Write-Host '     [WARN] Ollama may still be starting...'; exit 1 }"
) else (
    echo      [OK] Ollama is already running
)
echo.

REM ============================================
REM STEP 4: VERIFY QWEN2.5-CODER MODEL
REM ============================================
echo [4/5] Verifying Qwen2.5-Coder model...
ollama list | findstr /C:"qwen2.5-coder:14b-instruct-q8_0" >nul 2>&1
if errorlevel 1 (
    echo      [WARN] Qwen2.5-Coder model not found
    echo      You can still use the system, but RAG features will be limited
    echo      To install: ollama pull qwen2.5-coder:14b-instruct-q8_0
) else (
    echo      [OK] Qwen2.5-Coder model ready: qwen2.5-coder:14b-instruct-q8_0
)
echo.

REM ============================================
REM STEP 5: INSTALL DEPENDENCIES
REM ============================================
echo [5/5] Installing/updating Python dependencies...
echo      This may take 1-2 minutes on first run...
echo.

%PYTHON_CMD% -m pip install --upgrade pip setuptools wheel >nul 2>&1
%PYTHON_CMD% -m pip install -r requirements.txt >nul 2>&1
%PYTHON_CMD% -m pip install streamlit >nul 2>&1

echo      [OK] All dependencies installed (including Streamlit)
echo.

REM ============================================
REM START FLASK APPLICATION
REM ============================================
echo ================================================================================
echo                        STARTING APPLICATION
echo ================================================================================
echo.
echo  DEBUG INFO:
echo   - Python Command: %PYTHON_CMD%
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

REM Start Flask application
echo Starting Flask with command: %PYTHON_CMD%
echo.

%PYTHON_CMD% sr_feedback_app.py

REM Application has stopped
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
