@echo off
setlocal enabledelayedexpansion

title SR Feedback System - Multi-Model RAG (4 LLM Calls)

cls

echo ================================================================================
echo         SR Feedback System with MULTI-MODEL RAG Pipeline
echo         (4 LLM Calls: Workaround + Java Detection + Activity + Resolution)
echo ================================================================================
echo %date% %time%
echo.

REM ============================================
REM STEP 1: CHECK PYTHON (3.10-3.12 for numpy)
REM ============================================
echo [1/5] Checking Python installation...
set PYTHON_CMD=

REM Try py launcher with specific compatible versions
for /f "tokens=*" %%v in ('py -3.12 --version 2^>^&1') do set PY_CHECK=%%v
echo !PY_CHECK! | findstr /C:"Python 3.12" >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py -3.12
    goto :python_found
)

for /f "tokens=*" %%v in ('py -3.11 --version 2^>^&1') do set PY_CHECK=%%v
echo !PY_CHECK! | findstr /C:"Python 3.11" >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py -3.11
    goto :python_found
)

for /f "tokens=*" %%v in ('py -3.10 --version 2^>^&1') do set PY_CHECK=%%v
echo !PY_CHECK! | findstr /C:"Python 3.10" >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py -3.10
    goto :python_found
)

REM Try default python
for /f "tokens=*" %%v in ('python --version 2^>^&1') do set PY_CHECK=%%v
echo !PY_CHECK! | findstr /C:"Python 3.1" >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    goto :python_found
)

echo      [ERROR] Python 3.10-3.12 not found!
echo      Please run First_time_MultiModel.bat first
echo.
pause
exit /b 1

:python_found
for /f "tokens=*" %%i in ('!PYTHON_CMD! --version 2^>^&1') do set PYTHON_VERSION=%%i
echo      [OK] !PYTHON_VERSION! found
echo      [OK] Using command: !PYTHON_CMD!
echo.

REM ============================================
REM STEP 2: CHECK TOKENS FILE
REM ============================================
echo [2/5] Checking API tokens file...
if exist "tokens\Tokens.xlsx" (
    echo      [OK] tokens\Tokens.xlsx found
) else (
    echo      [ERROR] tokens\Tokens.xlsx not found!
    echo      Please create tokens\Tokens.xlsx with columns: email, Token
    echo.
    pause
    exit /b 1
)
echo.

REM ============================================
REM STEP 3: CHECK VIRTUAL ENVIRONMENT
REM ============================================
echo [3/5] Checking virtual environment...
set VENV_DIR=venv

if exist "%VENV_DIR%\Scripts\activate.bat" (
    echo      [OK] Virtual environment found
    call "%VENV_DIR%\Scripts\activate.bat"
    echo      [OK] Virtual environment activated
) else (
    echo      [WARN] Virtual environment not found - using system Python
    echo      [INFO] Run First_time_MultiModel.bat to create venv
)
echo.

REM ============================================
REM STEP 4: CHECK ALL DATABASES AND VECTOR STORES
REM ============================================
echo [4/5] Checking ALL databases and vector stores...
echo.

set DB_DIR=data\database
set VS_DIR=data\vectorstore
set WARN_COUNT=0
set ERROR_COUNT=0

echo      --- VECTOR STORES ---
REM Check ChromaDB (REQUIRED for semantic search)
if exist "%VS_DIR%\chromadb_store\chroma.sqlite3" (
    echo      [OK] ChromaDB vectorstore
) else if exist "%VS_DIR%\chromadb_store" (
    echo      [WARN] ChromaDB folder exists but may be empty
    set /a WARN_COUNT+=1
) else (
    echo      [ERROR] ChromaDB NOT FOUND - semantic search will NOT work!
    set /a ERROR_COUNT+=1
)

echo.
echo      --- DATABASES ---

REM Check abbreviation.db (REQUIRED)
if exist "%DB_DIR%\abbreviation.db" (
    echo      [OK] abbreviation.db
) else (
    echo      [ERROR] abbreviation.db NOT FOUND - abbreviation expansion will fail!
    set /a ERROR_COUNT+=1
)

REM Check people_skills.db (REQUIRED for team assignment)
if exist "%DB_DIR%\people_skills.db" (
    echo      [OK] people_skills.db
) else (
    echo      [WARN] people_skills.db not found - team assignment disabled
    set /a WARN_COUNT+=1
)

REM Check sr_tracking.db (REQUIRED for SR tracking)
if exist "%DB_DIR%\sr_tracking.db" (
    echo      [OK] sr_tracking.db
) else (
    echo      [WARN] sr_tracking.db not found - SR tracking disabled
    set /a WARN_COUNT+=1
)

REM Check workaround_feedback.db (REQUIRED for feedback)
if exist "%DB_DIR%\workaround_feedback.db" (
    echo      [OK] workaround_feedback.db
) else (
    echo      [WARN] workaround_feedback.db not found - feedback system disabled
    set /a WARN_COUNT+=1
)

REM Check llm_usage_stats.json (auto-created)
if exist "%DB_DIR%\llm_usage_stats.json" (
    echo      [OK] llm_usage_stats.json
) else (
    echo      [INFO] llm_usage_stats.json not found - will be created on first use
)

echo.
echo      --- SUMMARY ---
echo      Errors: !ERROR_COUNT!  Warnings: !WARN_COUNT!

if !ERROR_COUNT! GTR 0 (
    echo.
    echo      [ERROR] Critical files missing! Cannot start application.
    echo      Please ensure all required databases exist.
    echo.
    pause
    exit /b 1
)

if !WARN_COUNT! GTR 0 (
    echo      [WARN] Some features may not work properly.
)
echo.

REM ============================================
REM STEP 5: VERIFY DEPENDENCIES AND PIPELINE
REM ============================================
echo [5/5] Verifying dependencies and pipeline...

REM Quick Flask check
!PYTHON_CMD! -c "import flask" 2>nul
if errorlevel 1 (
    echo      [INFO] Installing dependencies...
    !PYTHON_CMD! -m pip install --upgrade pip setuptools wheel >nul 2>&1
    !PYTHON_CMD! -m pip install -r requirements.txt >nul 2>&1
    !PYTHON_CMD! -m pip install langchain langchain-core chromadb >nul 2>&1
)

!PYTHON_CMD! -c "import flask; print('      [OK] flask', flask.__version__)" 2>nul
if errorlevel 1 echo      [FAIL] flask not installed

!PYTHON_CMD! -c "import chromadb; print('      [OK] chromadb', chromadb.__version__)" 2>nul
if errorlevel 1 echo      [WARN] chromadb not installed

REM Test pipeline import (correct path: rag/pipeline)
echo      Testing Multi-Model pipeline...
!PYTHON_CMD! -c "import sys; sys.path.insert(0, 'rag/pipeline'); from multi_model_rag_pipeline_chatgpt import MultiModelSRPipeline; print('      [OK] Pipeline ready')" 2>nul
if errorlevel 1 (
    echo      [WARN] Pipeline import failed - will try anyway
)
echo.

REM ============================================
REM SET DATABASE CONFIGURATION (PostgreSQL)
REM ============================================
set DB_HOST=inoscmm2181
set DB_PORT=30432
set DB_NAME=paasdb
set DB_USER=ossdb01ref
set DB_PASSWORD=ossdb01ref

REM ============================================
REM START FLASK APPLICATION
REM ============================================
echo ================================================================================
echo                        STARTING APPLICATION
echo ================================================================================
echo.
echo  ENVIRONMENT:
echo   - Python: !PYTHON_VERSION!
echo   - Working Directory: %CD%
echo   - Virtual Env: %VENV_DIR%
echo.
echo  DATABASES LOADED:
echo   - ChromaDB vectorstore (semantic search)
echo   - abbreviation.db (abbreviations)
echo   - people_skills.db (team assignment)
echo   - sr_tracking.db (SR tracking)
echo   - workaround_feedback.db (user feedback)
echo.
echo  MULTI-MODEL ARCHITECTURE:
echo   - LLM Call 1: Find Semantic Workaround
echo   - LLM Call 2: Java Error Detection (5-Source Voting)
echo   - LLM Call 3: Activity Name Extraction
echo   - LLM Call 4: Final Resolution (Java or General)
echo.
echo  API CONFIGURATION:
echo   - API URL: https://ai-framework1:8085/api/v1/call_llm
echo   - Model: ChatGPT GPT-4.1
echo   - Token File: tokens\Tokens.xlsx
echo   - Daily Limit: $4 per token (auto-rotation)
echo.
echo ================================================================================
echo  ACCESS PORTALS:
echo ================================================================================
echo.
echo  USER PORTAL:  http://localhost:5000
echo    - Search SRs and view AI-generated workarounds
echo    - Vote on workarounds (thumbs up/down)
echo    - Provide feedback and corrections
echo.
echo  ADMIN PORTAL: http://localhost:5000/admin
echo    - Username: admin ^| Password: admin123
echo    - Upload Excel files for batch processing
echo    - View system statistics
echo.
echo ================================================================================
echo  Press Ctrl+C to stop the server
echo ================================================================================
echo.

echo Starting Flask...
echo.

!PYTHON_CMD! app\sr_feedback_app.py

echo.
echo ================================================================================
echo                        APPLICATION STOPPED
echo ================================================================================
echo %date% %time%
echo.
pause
endlocal
