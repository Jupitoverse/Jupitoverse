@echo off
setlocal enabledelayedexpansion

title SR Feedback System - First Time Setup (Multi-Model RAG)

cls

echo ================================================================================
echo         SR Feedback System - FIRST TIME SETUP
echo         (Multi-Model RAG Pipeline - 4 LLM Calls)
echo ================================================================================
echo %date% %time%
echo.
echo  This script will:
echo   1. Check/Install compatible Python (3.10-3.12)
echo   2. Install Python dependencies (LangChain + all requirements)
echo   3. Verify tokens\Tokens.xlsx file exists
echo   4. Verify vector stores exist
echo   5. Start the application
echo.
echo  NOTE: First time setup may take 5-10 minutes
echo        NO large model downloads required (uses cloud API)
echo.
echo ================================================================================
echo.

REM ============================================
REM STEP 1: CHECK/INSTALL PYTHON (3.10-3.12)
REM ============================================
echo [1/6] Checking Python installation...
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

REM Try default python
for /f "tokens=*" %%v in ('python --version 2^>^&1') do set PY_CHECK=%%v
echo !PY_CHECK! | findstr /C:"Python 3.1" >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    echo      [OK] Found compatible Python
    goto :python_found
)

REM No compatible Python found
echo      [ERROR] No compatible Python (3.10-3.12) found!
echo      Please install Python from: https://python.org/downloads/
echo.
pause
exit /b 1

:python_found
for /f "tokens=*" %%i in ('!PYTHON_CMD! --version 2^>^&1') do set PYTHON_VERSION=%%i
echo      [OK] !PYTHON_VERSION! - Compatible!
echo      [OK] Using command: !PYTHON_CMD!
echo.

REM ============================================
REM STEP 2: CHECK TOKENS FILE
REM ============================================
echo [2/6] Checking API tokens file...
echo.

if not exist "tokens\Tokens.xlsx" goto :tokens_not_found

echo      [OK] tokens\Tokens.xlsx found
!PYTHON_CMD! -c "import pandas as pd; df = pd.read_excel('tokens/Tokens.xlsx'); print('      [OK] Loaded', len(df), 'API tokens')" 2>nul
if errorlevel 1 echo      [WARN] Could not read tokens\Tokens.xlsx - will verify after dependencies install
goto :tokens_done

:tokens_not_found
echo      [ERROR] tokens\Tokens.xlsx NOT FOUND!
echo.
echo      ================================================================
echo       API TOKENS REQUIRED
echo      ================================================================
echo       Please create tokens\Tokens.xlsx with columns:
echo         - Name or email: user@amdocs.com
echo         - Token: your-api-token-here
echo.
echo       Each token has $4/day limit. Multiple tokens enable rotation.
echo      ================================================================
echo.
pause
exit /b 1

:tokens_done
echo.

REM ============================================
REM STEP 3: INSTALL PYTHON DEPENDENCIES
REM ============================================
echo [3/6] Installing/updating Python dependencies...
echo      This may take 2-5 minutes on first run...
echo.

!PYTHON_CMD! -m pip install --upgrade pip setuptools wheel >nul 2>&1

echo      Installing core requirements...
!PYTHON_CMD! -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo      [WARN] Some requirements failed, trying individually...
)

echo      Installing LangChain for ChatGPT...
!PYTHON_CMD! -m pip install "langchain>=1.0.0" "langchain-core>=1.0.0" "langchain-community>=0.3.0" --quiet
if errorlevel 1 (
    echo      [ERROR] Failed to install LangChain!
    pause
    exit /b 1
)

echo      [OK] All dependencies installed
echo.

REM ============================================
REM STEP 4: VERIFY DEPENDENCIES
REM ============================================
echo [4/6] Verifying dependencies...
echo.

!PYTHON_CMD! -c "import numpy; print('      [OK] numpy', numpy.__version__)" 2>nul
if errorlevel 1 echo      [FAIL] numpy not working

!PYTHON_CMD! -c "import pandas; print('      [OK] pandas', pandas.__version__)" 2>nul
if errorlevel 1 echo      [FAIL] pandas not working

!PYTHON_CMD! -c "import langchain; print('      [OK] langchain', langchain.__version__)" 2>nul
if errorlevel 1 echo      [FAIL] langchain not working

!PYTHON_CMD! -c "import sentence_transformers; print('      [OK] sentence_transformers', sentence_transformers.__version__)" 2>nul
if errorlevel 1 echo      [WARN] sentence_transformers not installed (will use fallback)

!PYTHON_CMD! -c "import chromadb; print('      [OK] chromadb', chromadb.__version__)" 2>nul
if errorlevel 1 (
    echo      [WARN] chromadb not installed - Installing now...
    !PYTHON_CMD! -m pip install chromadb --quiet
    !PYTHON_CMD! -c "import chromadb; print('      [OK] chromadb', chromadb.__version__)" 2>nul
    if errorlevel 1 echo      [ERROR] Failed to install chromadb - semantic search will NOT work!
)

!PYTHON_CMD! -c "import pandas as pd; df = pd.read_excel('tokens/Tokens.xlsx'); print('      [OK] API tokens:', len(df), 'loaded')" 2>nul
if errorlevel 1 echo      [FAIL] tokens\Tokens.xlsx not readable

echo.

REM ============================================
REM STEP 5: CHECK DATABASES AND VECTOR STORES
REM ============================================
echo [5/6] Checking databases in "data\database" folder...
echo.

set DB_DIR=data\database
set VS_DIR=data\vectorstore
set VS_OK=1

REM Check ChromaDB (primary vectorstore - replaces old .db files)
if exist "%VS_DIR%\chromadb_store\chroma.sqlite3" (
    echo      [OK] ChromaDB vectorstore found
) else (
    echo      [WARN] ChromaDB not found - semantic search may not work
    set VS_OK=0
)

REM Check required SQLite databases
if exist "%DB_DIR%\abbreviation.db" (
    echo      [OK] abbreviation.db found
) else (
    echo      [WARN] abbreviation.db not found
    set VS_OK=0
)

if exist "%DB_DIR%\people_skills.db" (
    echo      [OK] people_skills.db found
) else (
    echo      [WARN] people_skills.db not found - Team assignment may not work
)

if exist "%DB_DIR%\sr_tracking.db" (
    echo      [OK] sr_tracking.db found
) else (
    echo      [WARN] sr_tracking.db not found - SR tracking may not work
)

if exist "%DB_DIR%\workaround_feedback.db" (
    echo      [OK] workaround_feedback.db found
) else (
    echo      [WARN] workaround_feedback.db not found - Feedback may not work
)

if exist "data\llm_usage_stats.json" (
    echo      [OK] llm_usage_stats.json found
) else (
    echo      [INFO] llm_usage_stats.json not found - will be created on first use
)

echo.
echo      Testing Multi-Model pipeline import...
!PYTHON_CMD! -c "import sys; sys.path.insert(0, 'RAG/pipeline'); from multi_model_rag_pipeline_chatgpt import MultiModelSRPipeline; print('      [OK] Multi-Model pipeline ready')" 2>nul
if errorlevel 1 (
    echo      [WARN] Multi-Model pipeline import failed - check error messages above
)

echo.

REM ============================================
REM STEP 6: SET DATABASE CONFIGURATION
REM ============================================
echo [6/7] Setting database configuration...
set DB_HOST=inoscmm2181
set DB_PORT=30432
set DB_NAME=paasdb
set DB_USER=ossdb01ref
set DB_PASSWORD=ossdb01ref
echo      [OK] PostgreSQL config set (ActivityFinder enabled)
echo.

REM ============================================
REM STEP 7: START FLASK APPLICATION
REM ============================================
echo [7/7] Starting application...
echo.
echo ================================================================================
echo                        SETUP COMPLETE - STARTING APPLICATION
echo ================================================================================
echo.
echo  DEBUG INFO:
echo   - Python Command: !PYTHON_CMD!
echo   - Working Directory: %CD%
echo   - Pipeline: MULTI-MODEL RAG (4 LLM Calls)
echo   - LLM: ChatGPT GPT-4.1 (via AI Framework Proxy)
echo.
echo ================================================================================
echo  MULTI-MODEL ARCHITECTURE:
echo ================================================================================
echo.
echo   LLM Call 1: Find Semantic Workaround
echo      - If no good match found in semantic search
echo      - Uses historical SR database
echo.
echo   LLM Call 2: Java Error Detection (5-Source Voting)
echo      - Analyzes: Categories, Semantic WA, AI WAs, User WAs, Current SR
echo      - Votes: JAVA / NON_JAVA / UNKNOWN
echo      - Returns: is_java_error (boolean)
echo.
echo   LLM Call 3: Activity Name Extraction
echo      - Only if Java error detected
echo      - Extracts activity names from SR text
echo      - Retries up to 2 times if not found in DB
echo.
echo   LLM Call 4: Final Resolution
echo      - 4a: Java Resolution (with code context)
echo      - 4b: General Resolution (for non-Java issues)
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
echo  RAG FEATURES:
echo ================================================================================
echo   [x] 4 Focused LLM Calls (better accuracy)
echo   [x] 5-Source Voting for Java Detection
echo   [x] Activity Extraction with Retry Loop
echo   [x] Historical SR Matching (21,000+ SRs)
echo   [x] Java Backend Detection (11,795 classes)
echo   [x] User Feedback Learning
echo   [x] Automatic Token Rotation ($4/day limit)
echo.
echo ================================================================================
echo  API TOKEN INFO:
echo ================================================================================
echo   * Tokens loaded from: tokens\Tokens.xlsx
echo   * Each token has $4/day limit
echo   * System auto-rotates to next token on limit
echo   * Processing time: ~15-30 seconds per SR
echo.
echo ================================================================================
echo.

echo Starting Flask with command: !PYTHON_CMD!
echo.

!PYTHON_CMD! app\sr_feedback_app.py

echo.
echo ================================================================================
echo                        APPLICATION STOPPED
echo ================================================================================
echo.
echo %date% %time%
echo.
pause
endlocal

