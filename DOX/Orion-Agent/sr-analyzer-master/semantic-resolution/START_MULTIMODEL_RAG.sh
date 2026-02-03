#!/bin/bash

# SR Feedback System - Start Application (Multi-Model RAG)
# Quick start script - assumes First_time_MultiModel.sh was run before

# Exit on error with helpful message
set -e
trap 'echo ""; echo "[ERROR] Script failed at line $LINENO"; echo "Try running First_time_MultiModel.sh first."; read -p "Press Enter to exit..."' ERR

# Get script directory (works even when called from different location)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ============================================
# PROXY CONFIGURATION (Amdocs Corporate Network)
# ============================================
export HTTP_PROXY=http://genproxy.corp.amdocs.com:8080/
export http_proxy=http://genproxy.corp.amdocs.com:8080/
export HTTPS_PROXY=http://genproxy.corp.amdocs.com:8080/
export https_proxy=http://genproxy.corp.amdocs.com:8080/
export FTP_PROXY=http://genproxy.corp.amdocs.com:8080/
export ftp_proxy=http://genproxy.corp.amdocs.com:8080/
export no_proxy=localhost,127.0.0.1,.corp.amdocs.com,.amdocs.com,corp.amdocs.com,amdocs.com,localaddress,.localdomain.com,illinlic01,indlinsls,linvc04,illinmtx013,/var/run/docker.sock,.sock,ai-framework1
export NO_PROXY=localhost,127.0.0.1,.corp.amdocs.com,.amdocs.com,corp.amdocs.com,amdocs.com,localaddress,.localdomain.com,illinlic01,indlinsls,linvc04,illinmtx013,/var/run/docker.sock,.sock,ai-framework1
export no_http_proxy=localhost,127.0.0.1,.corp.amdocs.com,.amdocs.com,corp.amdocs.com,amdocs.com,localaddress,.localdomain.com,illinlic01,indlinsls,linvc04,illinmtx013,/var/run/docker.sock,.sock,ai-framework1

# ============================================
# AZURE AD CONFIGURATION
# ============================================
# Get hostname for Azure AD redirect URI
SERVER_HOSTNAME=$(hostname -f 2>/dev/null || hostname)
export AZURE_REDIRECT_URI="https://${SERVER_HOSTNAME}:5000/auth/microsoft/callback"

clear

echo "================================================================================"
echo "        SR Feedback System with MULTI-MODEL RAG Pipeline"
echo "        (4 LLM Calls: Workaround + Java Detection + Activity + Resolution)"
echo "================================================================================"
echo "$(date)"
echo ""

# ============================================
# STEP 1: CHECK PYTHON
# ============================================
echo "[1/4] Checking Python installation..."

# Function to find compatible Python
find_python() {
    local cmd version
    for cmd in python3.12 python3.11 python3.10 python3; do
        if command -v "$cmd" &>/dev/null; then
            version=$("$cmd" --version 2>&1)
            if [[ "$version" == *"3.10"* ]] || [[ "$version" == *"3.11"* ]] || [[ "$version" == *"3.12"* ]]; then
                echo "$cmd"
                return 0
            fi
        fi
    done
    return 1
}

PYTHON_CMD=$(find_python) || PYTHON_CMD=""

if [ -z "$PYTHON_CMD" ]; then
    echo "     [ERROR] Python 3.10-3.12 not found!"
    echo "     Please run First_time_MultiModel.sh first to install Python"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo "     [OK] $PYTHON_VERSION"
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
    read -p "Press Enter to exit..."
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
    
    $PYTHON_CMD -m venv "$VENV_DIR" || {
        echo "     [ERROR] Failed to create virtual environment!"
        echo "     Please run First_time_MultiModel.sh first"
        echo ""
        read -p "Press Enter to exit..."
        exit 1
    }
fi

# Check if activate script exists
if [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "     [ERROR] Virtual environment is broken!"
    echo "     Please delete 'venv' folder and run First_time_MultiModel.sh"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Activate virtual environment
set +e
source "$VENV_DIR/bin/activate"
ACTIVATE_RESULT=$?
set -e

if [ $ACTIVATE_RESULT -ne 0 ] || [ -z "$VIRTUAL_ENV" ]; then
    echo "     [ERROR] Failed to activate virtual environment!"
    echo "     Please run First_time_MultiModel.sh first"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "     [OK] Virtual environment activated"
echo ""

# ============================================
# STEP 4: QUICK DEPENDENCY CHECK
# ============================================
echo "[4/4] Verifying dependencies..."

# Set pip to use public PyPI (through proxy)
PIP_INDEX="--index-url https://pypi.org/simple/ --trusted-host pypi.org --trusted-host files.pythonhosted.org"

# Check if Flask is installed (quick test)
if ! python -c "import flask" 2>/dev/null; then
    echo "     [INFO] Dependencies not installed, installing now..."
    echo "     This may take 1-2 minutes..."
    
    pip install --upgrade pip setuptools wheel --quiet $PIP_INDEX 2>/dev/null || true
    
    # Filter out pywin32 (Windows-only) and install
    if [ -f "requirements.txt" ]; then
        grep -v "pywin32" requirements.txt > /tmp/requirements_linux.txt 2>/dev/null || cp requirements.txt /tmp/requirements_linux.txt
        pip install -r /tmp/requirements_linux.txt --quiet $PIP_INDEX 2>/dev/null || true
        rm -f /tmp/requirements_linux.txt
    fi
    
    pip install langchain langchain-core langchain-community --quiet $PIP_INDEX 2>/dev/null || true
    pip install chromadb sentence-transformers==2.2.2 --quiet $PIP_INDEX 2>/dev/null || true
    pip install pysqlite3-binary --quiet $PIP_INDEX 2>/dev/null || true
    pip install O365 --quiet $PIP_INDEX 2>/dev/null || true
fi

# Ensure SQLite fix exists and is applied
if [ ! -f "app/sqlite_fix.py" ]; then
    cat > app/sqlite_fix.py << 'SQLITEFIX'
# SQLite fix for older systems (RHEL/CentOS with SQLite < 3.35)
# This must be imported BEFORE chromadb
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass  # pysqlite3 not installed, use system sqlite3
SQLITEFIX
fi

# Add sqlite_fix import to sr_feedback_app.py if not already present
if ! grep -q "import sqlite_fix" app/sr_feedback_app.py 2>/dev/null; then
    sed -i '1i import sqlite_fix  # Fix for old SQLite on RHEL' app/sr_feedback_app.py
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
echo "  - Python: $PYTHON_VERSION"
echo "  - Virtual Env: $VENV_DIR"
echo "  - Working Directory: $(pwd)"
echo "  - Script: app/sr_feedback_app.py"
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
echo "  - Token File: tokens/Tokens.xlsx"
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
echo "Starting Flask application..."
echo ""

set +e
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
read -p "Press Enter to exit..."
