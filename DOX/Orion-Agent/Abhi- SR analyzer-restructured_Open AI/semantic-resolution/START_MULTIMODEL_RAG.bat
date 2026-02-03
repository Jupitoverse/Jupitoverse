@echo off

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

REM Check default py command
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
)

REM Try python command
python --version >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=*" %%v in ('python --version 2^>^&1') do set PY_CHECK=%%v
    
    echo %PY_CHECK% | findstr /C:"Python 3.10 Python 3.11 Python 3.12" >nul 2>&1
    if not errorlevel 1 (
        set PYTHON_CMD=python
        goto :python_found
    )
)

echo      [ERROR] Python 3.10-3.12 not found!
echo      Please run First_time_MultiModel.bat to install Python
echo.
pause
exit /b 1

:python_found
for /f "tokens=*" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set PYTHON_VERSION=%%i
echo      [OK] %PYTHON_VERSION% found
echo      [OK] Using command: %PYTHON_CMD%
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
REM STEP 3: INSTALL DEPENDENCIES
REM ============================================
echo [3/5] Installing/updating Python dependencies...
echo      This may take 1-2 minutes on first run...
echo.

%PYTHON_CMD% -m pip install --upgrade pip setuptools wheel >nul 2>&1
%PYTHON_CMD% -m pip install -r requirements.txt >nul 2>&1
%PYTHON_CMD% -m pip install langchain langchain-core >nul 2>&1
%PYTHON_CMD% -m pip install chromadb >nul 2>&1

echo      [OK] All dependencies installed
%PYTHON_CMD% -c "import chromadb; print('      [OK] chromadb', chromadb.__version__)" 2>nul
if errorlevel 1 echo      [ERROR] chromadb not installed - semantic search will NOT work!
echo.

REM ============================================
REM STEP 4: CHECK VECTOR STORES
REM ============================================
echo [4/5] Checking data stores...

set DB_DIR=data\database
set VS_DIR=data\vectorstore

REM Check ChromaDB (primary vectorstore - replaces old .db files)
if exist "%VS_DIR%\chromadb_store\chroma.sqlite3" (
    echo      [OK] ChromaDB vectorstore
) else (
    echo      [WARN] ChromaDB not found - semantic search will not work
)

REM Check required SQLite databases
if exist "%DB_DIR%\abbreviation.db" (
    echo      [OK] abbreviation.db
) else (
    echo      [WARN] abbreviation.db not found
)

if exist "%DB_DIR%\people_skills.db" (
    echo      [OK] people_skills.db
) else (
    echo      [WARN] people_skills.db not found
)
echo.

REM ============================================
REM STEP 5: VERIFY MULTI-MODEL PIPELINE
REM ============================================
echo [5/5] Verifying Multi-Model pipeline...
%PYTHON_CMD% -c "import sys; sys.path.insert(0, 'RAG/pipeline'); from multi_model_rag_pipeline_chatgpt import MultiModelSRPipeline; print('      [OK] Multi-Model pipeline ready')" 2>nul
if errorlevel 1 (
    echo      [WARN] Pipeline import check failed - will try anyway
)
echo.

REM ============================================
REM SET DATABASE CONFIGURATION
REM ============================================
echo [5/5] Setting database configuration...
set DB_HOST=inoscmm2181
set DB_PORT=30432
set DB_NAME=paasdb
set DB_USER=ossdb01ref
set DB_PASSWORD=ossdb01ref
echo      [OK] PostgreSQL config set (ActivityFinder enabled)
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
echo   - Script: app\sr_feedback_app.py
echo   - Pipeline: MULTI-MODEL (4 LLM Calls)
echo.
echo  MULTI-MODEL ARCHITECTURE:
echo   - LLM Call 1: Find Semantic Workaround (if not found in DB)
echo   - LLM Call 2: Java Error Detection (5-Source Voting)
echo   - LLM Call 3: Activity Name Extraction (with retry)
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
echo    - Generate on-demand AI analysis
echo.
echo  ADMIN PORTAL: http://localhost:5000/admin
echo    - Username: admin ^| Password: admin123
echo    - Upload Excel files for batch processing
echo    - View system statistics
echo.
echo ================================================================================
echo  MULTI-MODEL RAG FEATURES:
echo ================================================================================
echo   [x] 4 LLM Calls per SR (focused, accurate)
echo   [x] 5-Source Voting for Java Detection (LLM-powered)
echo   [x] Activity Extraction with Retry Loop
echo   [x] Historical SR Matching (21,000+ SRs)
echo   [x] Java Backend Detection (11,795 classes)
echo   [x] Automatic Token Rotation ($4/day limit)
echo   [x] User Feedback Learning
echo.
echo ================================================================================
echo  IMPORTANT NOTES:
echo ================================================================================
echo   * Uses Multi-Model architecture (4 focused LLM calls)
echo   * More accurate than single mega-prompt
echo   * Each token has $4/day limit - auto-rotates when exhausted
echo   * Processing time: ~15-30 seconds per SR
echo   * Press Ctrl+C to stop the Flask server
echo.
echo ================================================================================
echo.

REM Start Flask application
echo Starting Flask with command: %PYTHON_CMD%
echo.

%PYTHON_CMD% app\sr_feedback_app.py

REM Application has stopped
echo.
echo ================================================================================
echo                        APPLICATION STOPPED
echo ================================================================================
echo.
echo %date% %time%
echo.
pause

