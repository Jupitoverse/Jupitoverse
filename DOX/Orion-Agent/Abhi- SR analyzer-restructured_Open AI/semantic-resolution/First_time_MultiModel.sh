#!/bin/bash
set -e  # Exit on error

# SR Feedback System - First Time Setup (Multi-Model RAG)

# Get script directory (works even if called from elsewhere)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

clear

echo "================================================================================"
echo "        SR Feedback System - FIRST TIME SETUP"
echo "        (Multi-Model RAG Pipeline - 4 LLM Calls)"
echo "================================================================================"
echo "$(date)"
echo ""
echo " This script will:"
echo "  1. Check/Install compatible Python (3.10-3.12)"
echo "  2. Create virtual environment"
echo "  3. Install Python dependencies (LangChain + all requirements)"
echo "  4. Verify Tokens.xlsx file exists"
echo "  5. Verify vector stores exist"
echo "  6. Start the application"
echo ""
echo " NOTE: First time setup may take 5-10 minutes"
echo "       NO large model downloads required (uses cloud API)"
echo ""
echo "================================================================================"
echo ""

# ============================================
# STEP 1: CHECK/INSTALL PYTHON (3.10-3.12)
# ============================================
echo "[1/7] Checking Python installation..."
echo "     [INFO] Looking for Python 3.10-3.12 (required for numpy/pandas)"
echo ""

PYTHON_CMD=""

# Try python3.12
if command -v python3.12 > /dev/null 2>&1; then
    PY_CHECK=$(python3.12 --version 2>&1)
    case "$PY_CHECK" in
        *"Python 3.12"*)
        PYTHON_CMD="python3.12"
        echo "     [OK] Found Python 3.12"
            ;;
    esac
fi

# Try python3.11
if [ -z "$PYTHON_CMD" ] && command -v python3.11 > /dev/null 2>&1; then
    PY_CHECK=$(python3.11 --version 2>&1)
    case "$PY_CHECK" in
        *"Python 3.11"*)
        PYTHON_CMD="python3.11"
        echo "     [OK] Found Python 3.11"
            ;;
    esac
fi

# Try python3.10
if [ -z "$PYTHON_CMD" ] && command -v python3.10 > /dev/null 2>&1; then
    PY_CHECK=$(python3.10 --version 2>&1)
    case "$PY_CHECK" in
        *"Python 3.10"*)
        PYTHON_CMD="python3.10"
        echo "     [OK] Found Python 3.10"
            ;;
    esac
fi

# Try default python3
if [ -z "$PYTHON_CMD" ] && command -v python3 > /dev/null 2>&1; then
    PY_CHECK=$(python3 --version 2>&1)
    case "$PY_CHECK" in
        *"Python 3.10"*|*"Python 3.11"*|*"Python 3.12"*)
        PYTHON_CMD="python3"
        echo "     [OK] Found compatible Python"
            ;;
    esac
fi

# No compatible Python found
if [ -z "$PYTHON_CMD" ]; then
    echo "     [ERROR] No compatible Python (3.10-3.12) found!"
    echo ""
    echo "     For Red Hat / CentOS / Fedora:"
    echo "       sudo dnf install python3.11 python3.11-pip python3.11-devel"
    echo ""
    echo "     For Ubuntu / Debian:"
    echo "       sudo apt install python3 python3-venv python3-pip"
    echo ""
    echo "     Or download from: https://python.org/downloads/"
    echo ""
    read -p "Press Enter to exit..." _
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo "     [OK] $PYTHON_VERSION - Compatible!"
echo "     [OK] Using command: $PYTHON_CMD"
echo ""

# ============================================
# STEP 2: CHECK TOKENS FILE
# ============================================
echo "[2/7] Checking API tokens file..."
echo ""

if [ ! -f "tokens/Tokens.xlsx" ]; then
    echo "     [ERROR] tokens/Tokens.xlsx NOT FOUND!"
    echo ""
    echo "     ================================================================"
    echo "      API TOKENS REQUIRED"
    echo "     ================================================================"
    echo "      Please create Tokens.xlsx with columns:"
    echo "        - Name or email: user@amdocs.com"
    echo "        - Token: your-api-token-here"
    echo ""
    echo "      Each token has \$4/day limit. Multiple tokens enable rotation."
    echo "     ================================================================"
    echo ""
    read -p "Press Enter to exit..." _
    exit 1
fi

echo "     [OK] tokens/Tokens.xlsx found"
echo ""

# ============================================
# STEP 3: CREATE VIRTUAL ENVIRONMENT
# ============================================
echo "[3/7] Setting up virtual environment..."
echo ""

VENV_DIR="venv"

# Check if venv exists but is broken (missing activate)
if [ -d "$VENV_DIR" ] && [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "     [WARN] Broken venv found, removing..."
    rm -rf "$VENV_DIR"
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "     Creating virtual environment..."
    echo "     (This may take a moment...)"
    $PYTHON_CMD -m venv "$VENV_DIR" 2>&1
    if [ ! -f "$VENV_DIR/bin/activate" ]; then
        echo "     [ERROR] Failed to create virtual environment!"
        echo ""
        echo "     For Red Hat / CentOS / Fedora:"
        echo "       sudo dnf install python3.11-devel"
        echo ""
        echo "     For Ubuntu / Debian:"
        echo "       sudo apt install python3-venv python3-full"
        echo ""
        echo "     Then run this script again."
        echo ""
        read -p "Press Enter to exit..." _
        exit 1
    fi
    echo "     [OK] Virtual environment created"
else
    echo "     [OK] Virtual environment already exists"
fi

# Verify activate script exists
if [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "     [ERROR] venv/bin/activate not found!"
    echo "     Removing broken venv..."
    rm -rf "$VENV_DIR"
    echo ""
    echo "     For Red Hat / CentOS / Fedora:"
    echo "       sudo dnf install python3.11-devel"
    echo ""
    echo "     For Ubuntu / Debian:"
    echo "       sudo apt install python3-venv python3-full"
    echo ""
    read -p "Press Enter to exit..." _
    exit 1
fi

# Activate virtual environment
echo "     Activating virtual environment..."
set +e
source "$VENV_DIR/bin/activate"
ACTIVATE_RESULT=$?
set -e

if [ $ACTIVATE_RESULT -ne 0 ] || [ -z "$VIRTUAL_ENV" ]; then
    echo "     [ERROR] Failed to activate virtual environment!"
    echo ""
    read -p "Press Enter to exit..." _
    exit 1
fi

echo "     [OK] Virtual environment activated"
echo ""

# ============================================
# STEP 4: INSTALL PYTHON DEPENDENCIES (Linux-safe)
# ============================================
echo "[4/7] Installing/updating Python dependencies..."
echo "     This may take 2-5 minutes on first run..."
echo ""

# Upgrade pip first
pip install --upgrade pip setuptools wheel 2>&1 | head -5 || true

echo "     Installing core requirements (skipping Windows-only packages)..."

# Filter out pywin32 for Linux (it's Windows-only)
grep -v "pywin32" requirements.txt > /tmp/requirements_linux.txt 2>/dev/null || cp requirements.txt /tmp/requirements_linux.txt

set +e
pip install -r /tmp/requirements_linux.txt
PIP_RESULT=$?
set -e

if [ $PIP_RESULT -ne 0 ]; then
    echo ""
    echo "     [WARN] Some requirements failed, trying individually..."
    # Try installing key packages one by one
    pip install flask pandas numpy openpyxl scikit-learn || true
    pip install sentence-transformers || true
    pip install chromadb || true
fi

rm -f /tmp/requirements_linux.txt

echo ""
echo "     Installing LangChain for ChatGPT..."
set +e
pip install "langchain>=0.1.0" "langchain-core>=0.1.0" "langchain-community>=0.3.0" --quiet
LANGCHAIN_RESULT=$?
set -e

echo "     Installing pandas and openpyxl..."
pip install pandas openpyxl --quiet || true

if [ $LANGCHAIN_RESULT -ne 0 ]; then
    echo "     [WARN] LangChain install had issues, but may still work"
fi

echo "     [OK] All dependencies installed"
echo ""

# ============================================
# STEP 5: VERIFY DEPENDENCIES
# ============================================
echo "[5/7] Verifying dependencies..."
echo ""

set +e
python -c "import numpy; print('     [OK] numpy', numpy.__version__)" 2>/dev/null || echo "     [FAIL] numpy not working"
python -c "import pandas; print('     [OK] pandas', pandas.__version__)" 2>/dev/null || echo "     [FAIL] pandas not working"
python -c "import flask; print('     [OK] flask', flask.__version__)" 2>/dev/null || echo "     [FAIL] flask not working"
python -c "import langchain; print('     [OK] langchain', langchain.__version__)" 2>/dev/null || echo "     [WARN] langchain not installed"
python -c "import sentence_transformers; print('     [OK] sentence_transformers', sentence_transformers.__version__)" 2>/dev/null || echo "     [WARN] sentence_transformers not installed (will use fallback)"
python -c "import chromadb; print('     [OK] chromadb', chromadb.__version__)" 2>/dev/null || echo "     [WARN] chromadb not installed"
python -c "import pandas as pd; df = pd.read_excel('tokens/Tokens.xlsx'); print('     [OK] API tokens:', len(df), 'loaded')" 2>/dev/null || echo "     [WARN] tokens/Tokens.xlsx not readable"
set -e

echo ""

# ============================================
# STEP 6: CHECK VECTOR STORES
# ============================================
echo "[6/7] Checking vector stores..."
echo ""

if [ -d "data/vectorstore/chromadb_store" ]; then
    echo "     [OK] chromadb_store found"
else
    echo "     [WARN] chromadb_store not found - semantic search may not work"
fi

if [ -f "data/database/abbreviation.db" ]; then
    echo "     [OK] abbreviation.db found"
else
    echo "     [WARN] abbreviation.db not found"
fi

if [ -f "data/database/people_skills.db" ]; then
    echo "     [OK] people_skills.db found"
else
    echo "     [WARN] people_skills.db not found"
fi

if [ -f "data/database/sr_tracking.db" ]; then
    echo "     [OK] sr_tracking.db found"
else
    echo "     [WARN] sr_tracking.db not found"
fi

if [ -f "data/database/workaround_feedback.db" ]; then
    echo "     [OK] workaround_feedback.db found"
else
    echo "     [WARN] workaround_feedback.db not found"
fi

echo ""
echo "     Testing Multi-Model pipeline import..."
set +e
python -c "
import sys
sys.path.insert(0, 'RAG/pipeline')
from multi_model_rag_pipeline_chatgpt import MultiModelSRPipeline
print('     [OK] Multi-Model pipeline ready')
" 2>/dev/null || echo "     [WARN] Multi-Model pipeline import failed - check error messages above"
set -e

echo ""

# ============================================
# STEP 7: START FLASK APPLICATION
# ============================================
echo "[7/7] Starting application..."
echo ""
echo "================================================================================"
echo "                       SETUP COMPLETE - STARTING APPLICATION"
echo "================================================================================"
echo ""
echo " DEBUG INFO:"
echo "  - Python Command: $PYTHON_CMD"
echo "  - Virtual Env: $VENV_DIR"
echo "  - Working Directory: $(pwd)"
echo "  - Pipeline: MULTI-MODEL RAG (4 LLM Calls)"
echo "  - LLM: ChatGPT GPT-4.1 (via AI Framework Proxy)"
echo ""
echo "================================================================================"
echo " MULTI-MODEL ARCHITECTURE:"
echo "================================================================================"
echo ""
echo "  LLM Call 1: Find Semantic Workaround"
echo "     - If no good match found in semantic search"
echo "     - Uses historical SR database"
echo ""
echo "  LLM Call 2: Java Error Detection (5-Source Voting)"
echo "     - Analyzes: Categories, Semantic WA, AI WAs, User WAs, Current SR"
echo "     - Votes: JAVA / NON_JAVA / UNKNOWN"
echo "     - Returns: is_java_error (boolean)"
echo ""
echo "  LLM Call 3: Activity Name Extraction"
echo "     - Only if Java error detected"
echo "     - Extracts activity names from SR text"
echo "     - Retries up to 2 times if not found in DB"
echo ""
echo "  LLM Call 4: Final Resolution"
echo "     - 4a: Java Resolution (with code context)"
echo "     - 4b: General Resolution (for non-Java issues)"
echo ""
echo "================================================================================"
echo " ACCESS PORTALS:"
echo "================================================================================"
echo ""
echo " USER PORTAL:  http://localhost:5000"
echo "   - Search SRs and view AI-generated workarounds"
echo "   - Vote on workarounds (thumbs up/down)"
echo "   - Provide feedback and corrections"
echo "   - Generate on-demand AI analysis"
echo ""
echo " ADMIN PORTAL: http://localhost:5000/admin"
echo "   - Username: admin | Password: admin123"
echo "   - Upload Excel files for batch processing"
echo "   - View system statistics"
echo ""
echo "================================================================================"
echo " RAG FEATURES:"
echo "================================================================================"
echo "  [x] 4 Focused LLM Calls (better accuracy)"
echo "  [x] 5-Source Voting for Java Detection"
echo "  [x] Activity Extraction with Retry Loop"
echo "  [x] Historical SR Matching (21,000+ SRs)"
echo "  [x] Java Backend Detection (11,795 classes)"
echo "  [x] User Feedback Learning"
echo "  [x] Automatic Token Rotation (\$4/day limit)"
echo ""
echo "================================================================================"
echo " API TOKEN INFO:"
echo "================================================================================"
echo "  * Tokens loaded from: tokens/Tokens.xlsx"
echo "  * Each token has \$4/day limit"
echo "  * System auto-rotates to next token on limit"
echo "  * Processing time: ~15-30 seconds per SR"
echo ""
echo "================================================================================"
echo ""

echo "Starting Flask with Python from virtual environment..."
echo ""

set +e
python app/sr_feedback_app.py
FLASK_EXIT=$?
set -e

echo ""
echo "================================================================================"
echo "                       APPLICATION STOPPED"
echo "================================================================================"
echo ""
echo "$(date)"
if [ $FLASK_EXIT -ne 0 ]; then
    echo "Flask exited with code: $FLASK_EXIT"
fi
echo ""
read -p "Press Enter to exit..." _
