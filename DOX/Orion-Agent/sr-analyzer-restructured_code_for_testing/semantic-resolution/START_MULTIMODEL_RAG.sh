#!/bin/bash
set -e  # Exit on error

# SR Feedback System - Multi-Model RAG (4 LLM Calls)

# Get script directory (works even if called from elsewhere)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

clear

echo "================================================================================"
echo "        SR Feedback System with MULTI-MODEL RAG Pipeline"
echo "        (4 LLM Calls: Workaround + Java Detection + Activity + Resolution)"
echo "================================================================================"
echo "$(date)"
echo ""

# ============================================
# STEP 1: CHECK PYTHON (3.10-3.12 for numpy)
# ============================================
echo "[1/4] Checking Python installation..."
PYTHON_CMD=""

# Try python3.12
if command -v python3.12 > /dev/null 2>&1; then
    PY_CHECK=$(python3.12 --version 2>&1)
    case "$PY_CHECK" in
        *"Python 3.12"*)
            PYTHON_CMD="python3.12"
            ;;
    esac
fi

# Try python3.11
if [ -z "$PYTHON_CMD" ] && command -v python3.11 > /dev/null 2>&1; then
    PY_CHECK=$(python3.11 --version 2>&1)
    case "$PY_CHECK" in
        *"Python 3.11"*)
            PYTHON_CMD="python3.11"
            ;;
    esac
fi

# Try python3.10
if [ -z "$PYTHON_CMD" ] && command -v python3.10 > /dev/null 2>&1; then
    PY_CHECK=$(python3.10 --version 2>&1)
    case "$PY_CHECK" in
        *"Python 3.10"*)
            PYTHON_CMD="python3.10"
            ;;
    esac
fi

# Try default python3
if [ -z "$PYTHON_CMD" ] && command -v python3 > /dev/null 2>&1; then
    PY_CHECK=$(python3 --version 2>&1)
    case "$PY_CHECK" in
        *"Python 3.10"*|*"Python 3.11"*|*"Python 3.12"*)
            PYTHON_CMD="python3"
            ;;
    esac
fi

# No compatible Python found
if [ -z "$PYTHON_CMD" ]; then
    echo "     [ERROR] Python 3.10-3.12 not found!"
    echo "     Please run First_time_MultiModel.sh first"
    echo ""
    read -p "Press Enter to exit..." _
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo "     [OK] $PYTHON_VERSION found"
echo "     [OK] Using command: $PYTHON_CMD"
echo ""

# ============================================
# STEP 2: CHECK TOKENS FILE
# ============================================
echo "[2/4] Checking API tokens file..."
if [ -f "tokens/Tokens.xlsx" ]; then
    echo "     [OK] tokens/Tokens.xlsx found"
else
    echo "     [ERROR] tokens/Tokens.xlsx not found!"
    echo "     Please create tokens/Tokens.xlsx with columns: email, Token"
    echo ""
    read -p "Press Enter to exit..." _
    exit 1
fi
echo ""

# ============================================
# STEP 3: ACTIVATE VIRTUAL ENVIRONMENT
# ============================================
echo "[3/4] Activating virtual environment..."

VENV_DIR="venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "     [WARN] Virtual environment not found!"
    echo "     Creating virtual environment..."
    $PYTHON_CMD -m venv "$VENV_DIR"
    if [ ! -f "$VENV_DIR/bin/activate" ]; then
        echo "     [ERROR] Failed to create virtual environment!"
        echo "     Please run First_time_MultiModel.sh first"
        echo ""
        read -p "Press Enter to exit..." _
        exit 1
    fi
fi

# Activate virtual environment
set +e  # Temporarily disable exit on error for source
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
# STEP 4: QUICK DEPENDENCY CHECK (Linux-safe)
# ============================================
echo "[4/4] Verifying dependencies..."

# Check if dependencies are installed, if not install them
set +e
python -c "import flask" 2>/dev/null
FLASK_CHECK=$?
set -e

if [ $FLASK_CHECK -ne 0 ]; then
    echo "     [INFO] Installing dependencies..."
    pip install --upgrade pip setuptools wheel 2>&1 | grep -v "already satisfied" || true
    # Skip pywin32 on Linux (Windows-only)
    grep -v "pywin32" requirements.txt > /tmp/requirements_linux.txt 2>/dev/null || cp requirements.txt /tmp/requirements_linux.txt
    pip install -r /tmp/requirements_linux.txt 2>&1 | grep -v "already satisfied" || true
    pip install langchain langchain-core langchain-community 2>&1 | grep -v "already satisfied" || true
    rm -f /tmp/requirements_linux.txt
fi

echo "     [OK] Dependencies ready"
echo ""

# ============================================
# START FLASK APPLICATION
# ============================================
echo "================================================================================"
echo "                       STARTING APPLICATION"
echo "================================================================================"
echo ""
echo " DEBUG INFO:"
echo "  - Python Command: $PYTHON_CMD"
echo "  - Virtual Env: $VENV_DIR"
echo "  - Working Directory: $(pwd)"
echo "  - Script: sr_feedback_app.py"
echo "  - Pipeline: MULTI-MODEL (4 LLM Calls)"
echo ""
echo " MULTI-MODEL ARCHITECTURE:"
echo "  - LLM Call 1: Find Semantic Workaround (if not found in DB)"
echo "  - LLM Call 2: Java Error Detection (5-Source Voting)"
echo "  - LLM Call 3: Activity Name Extraction (with retry)"
echo "  - LLM Call 4: Final Resolution (Java or General)"
echo ""
echo " API CONFIGURATION:"
echo "  - API URL: https://ai-framework1:8085/api/v1/call_llm"
echo "  - Model: ChatGPT GPT-4.1"
echo "  - Token File: Tokens.xlsx"
echo "  - Daily Limit: \$4 per token (auto-rotation)"
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
echo " MULTI-MODEL RAG FEATURES:"
echo "================================================================================"
echo "  [x] 4 LLM Calls per SR (focused, accurate)"
echo "  [x] 5-Source Voting for Java Detection (LLM-powered)"
echo "  [x] Activity Extraction with Retry Loop"
echo "  [x] Historical SR Matching (21,000+ SRs)"
echo "  [x] Java Backend Detection (11,795 classes)"
echo "  [x] Automatic Token Rotation (\$4/day limit)"
echo "  [x] User Feedback Learning"
echo ""
echo "================================================================================"
echo " IMPORTANT NOTES:"
echo "================================================================================"
echo "  * Uses Multi-Model architecture (4 focused LLM calls)"
echo "  * More accurate than single mega-prompt"
echo "  * Each token has \$4/day limit - auto-rotates when exhausted"
echo "  * Processing time: ~15-30 seconds per SR"
echo "  * Press Ctrl+C to stop the Flask server"
echo ""
echo "================================================================================"
echo ""

# Start Flask application
echo "Starting Flask with Python from virtual environment..."
echo ""

set +e  # Allow Flask to exit without triggering script error
python app/sr_feedback_app.py
FLASK_EXIT=$?
set -e

# Application has stopped
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
