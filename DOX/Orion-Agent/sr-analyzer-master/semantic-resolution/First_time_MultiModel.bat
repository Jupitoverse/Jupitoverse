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
echo   2. Create virtual environment (isolated dependencies)
echo   3. Install Python dependencies (LangChain + all requirements)
echo   4. Verify tokens\Tokens.xlsx file exists
echo   5. Check ALL databases and vector stores
echo   6. Start the application
echo.
echo  NOTE: First time setup may take 5-10 minutes
echo        NO large model downloads required (uses cloud API)
echo.
echo ================================================================================
echo.

REM ============================================
REM STEP 1: CHECK/INSTALL PYTHON (3.10-3.12)
REM ============================================
echo [1/7] Checking Python installation...
echo      [INFO] Looking for Python 3.10-3.12 (required for numpy/pandas)
echo.
set PYTHON_CMD=

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
echo [2/7] Checking API tokens file...
echo.

if not exist "tokens\Tokens.xlsx" goto :tokens_not_found

echo      [OK] tokens\Tokens.xlsx found
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
REM STEP 3: CREATE VIRTUAL ENVIRONMENT
REM ============================================
echo [3/7] Setting up virtual environment...
echo      [INFO] Virtual environments isolate project dependencies
echo.

set VENV_DIR=venv

if exist "%VENV_DIR%\Scripts\activate.bat" (
    echo      [OK] Virtual environment already exists
    goto :venv_activate
)

echo      Creating virtual environment...
echo      (This may take a moment...)
!PYTHON_CMD! -m venv "%VENV_DIR%"
if errorlevel 1 (
    echo      [ERROR] Failed to create virtual environment!
    echo      Try running: !PYTHON_CMD! -m pip install --upgrade pip
    pause
    exit /b 1
)
echo      [OK] Virtual environment created

:venv_activate
echo      Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo      [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)
echo      [OK] Virtual environment activated
echo.

REM ============================================
REM STEP 4: INSTALL PYTHON DEPENDENCIES
REM ============================================
echo [4/7] Installing/updating Python dependencies...
echo      This may take 2-5 minutes on first run...
echo.

echo      Upgrading pip...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1

echo      Installing core requirements...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo      [WARN] Some requirements failed, trying essential packages...
    python -m pip install flask pandas numpy openpyxl scikit-learn requests tqdm
)

echo      Installing LangChain for ChatGPT...
python -m pip install "langchain>=0.1.0" "langchain-core>=0.1.0" "langchain-community>=0.3.0" --quiet
if errorlevel 1 (
    echo      [WARN] LangChain install had issues, trying again...
    python -m pip install langchain langchain-core langchain-community
)

echo      Installing ChromaDB...
python -m pip install chromadb --quiet

echo      Installing sentence-transformers...
python -m pip install sentence-transformers --quiet

echo.
echo      [OK] All dependencies installed
echo.

REM ============================================
REM STEP 5: VERIFY DEPENDENCIES
REM ============================================
echo [5/7] Verifying dependencies...
echo.

python -c "import flask; print('      [OK] flask', flask.__version__)" 2>nul
if errorlevel 1 echo      [FAIL] flask not installed

python -c "import pandas; print('      [OK] pandas', pandas.__version__)" 2>nul
if errorlevel 1 echo      [FAIL] pandas not installed

python -c "import numpy; print('      [OK] numpy', numpy.__version__)" 2>nul
if errorlevel 1 echo      [FAIL] numpy not installed

python -c "import openpyxl; print('      [OK] openpyxl', openpyxl.__version__)" 2>nul
if errorlevel 1 echo      [FAIL] openpyxl not installed

python -c "import langchain; print('      [OK] langchain', langchain.__version__)" 2>nul
if errorlevel 1 echo      [WARN] langchain not installed

python -c "import chromadb; print('      [OK] chromadb', chromadb.__version__)" 2>nul
if errorlevel 1 (
    echo      [WARN] chromadb not installed - Installing now...
    python -m pip install chromadb --quiet
    python -c "import chromadb; print('      [OK] chromadb', chromadb.__version__)" 2>nul
    if errorlevel 1 echo      [ERROR] Failed to install chromadb!
)

python -c "import sentence_transformers; print('      [OK] sentence_transformers')" 2>nul
if errorlevel 1 echo      [WARN] sentence_transformers not installed

echo.
python -c "import pandas as pd; df = pd.read_excel('tokens/Tokens.xlsx'); print('      [OK] API tokens:', len(df), 'loaded')" 2>nul
if errorlevel 1 echo      [WARN] Could not read tokens\Tokens.xlsx

echo.

REM ============================================
REM STEP 6: CHECK ALL DATABASES AND VECTOR STORES
REM ============================================
echo [6/7] Checking ALL databases and vector stores...
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

REM Check people_skills.db (for team assignment)
if exist "%DB_DIR%\people_skills.db" (
    echo      [OK] people_skills.db
) else (
    echo      [WARN] people_skills.db not found - team assignment disabled
    set /a WARN_COUNT+=1
)

REM Check sr_tracking.db (for SR tracking)
if exist "%DB_DIR%\sr_tracking.db" (
    echo      [OK] sr_tracking.db
) else (
    echo      [WARN] sr_tracking.db not found - SR tracking disabled
    set /a WARN_COUNT+=1
)

REM Check workaround_feedback.db (for feedback)
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
    echo      [ERROR] Critical files missing!
    echo      The application may not work properly without these files.
    echo      Continuing anyway - check warnings above.
)

if !WARN_COUNT! GTR 0 (
    echo      [WARN] Some features may not work properly.
)
echo.

REM Check pipeline files exist (quick check, no heavy import)
echo      Checking Multi-Model pipeline files...
if exist "rag\pipeline\multi_model_rag_pipeline_chatgpt.py" (
    echo      [OK] multi_model_rag_pipeline_chatgpt.py found
) else (
    echo      [WARN] Pipeline file not found at rag\pipeline\
)
if exist "rag\pipeline\activity_name_finder.py" (
    echo      [OK] activity_name_finder.py found
) else (
    echo      [WARN] activity_name_finder.py not found
)
echo.

REM ============================================
REM STEP 7: SET DATABASE CONFIGURATION AND START
REM ============================================
echo [7/7] Starting application...
echo.

REM Set PostgreSQL configuration
set DB_HOST=inoscmm2181
set DB_PORT=30432
set DB_NAME=paasdb
set DB_USER=ossdb01ref
set DB_PASSWORD=ossdb01ref

echo ================================================================================
echo                        SETUP COMPLETE - STARTING APPLICATION
echo ================================================================================
echo.
echo  ENVIRONMENT:
echo   - Python: !PYTHON_VERSION!
echo   - Virtual Env: %VENV_DIR%
echo   - Working Directory: %CD%
echo   - Pipeline: MULTI-MODEL RAG (4 LLM Calls)
echo.
echo  DATABASES LOADED:
echo   - ChromaDB vectorstore (semantic search)
echo   - abbreviation.db (abbreviations)
echo   - people_skills.db (team assignment)
echo   - sr_tracking.db (SR tracking)
echo   - workaround_feedback.db (user feedback)
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
echo.
echo   LLM Call 3: Activity Name Extraction
echo      - Only if Java error detected
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
echo.
echo  ADMIN PORTAL: http://localhost:5000/admin
echo    - Username: admin ^| Password: admin123
echo    - Upload Excel files for batch processing
echo    - View system statistics
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
echo  Press Ctrl+C to stop the server
echo ================================================================================
echo.

echo Starting Flask...
echo.

python app\sr_feedback_app.py

echo.
echo ================================================================================
echo                        APPLICATION STOPPED
echo ================================================================================
echo %date% %time%
echo.
pause
endlocal
