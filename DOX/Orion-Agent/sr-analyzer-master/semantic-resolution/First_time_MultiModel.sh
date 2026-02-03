#!/bin/bash

# SR Feedback System - First Time Setup (Multi-Model RAG)
# Robust version for: Red Hat, CentOS, Fedora, Ubuntu, Debian

# Exit on error with helpful message
set -e
trap 'echo ""; echo "[ERROR] Script failed at line $LINENO"; echo "Check the error message above for details."; read -p "Press Enter to exit..."' ERR

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
echo "[INFO] Azure AD Redirect URI: $AZURE_REDIRECT_URI"

clear

echo "================================================================================"
echo "        SR Feedback System - FIRST TIME SETUP"
echo "        (Multi-Model RAG Pipeline - 4 LLM Calls)"
echo "================================================================================"
echo "$(date)"
echo ""
echo " This script will:"
echo "  1. Detect your Linux distribution"
echo "  2. Check/Install Python 3.10-3.12"
echo "  3. Create virtual environment (isolated dependencies)"
echo "  4. Install all Python packages"
echo "  5. Verify tokens/Tokens.xlsx"
echo "  6. Check databases and vector stores"
echo "  7. Start the application"
echo ""
echo " NOTE: First time setup may take 5-10 minutes"
echo "       You may be prompted for sudo password to install Python"
echo ""
echo "================================================================================"
echo ""

# ============================================
# STEP 1: DETECT LINUX DISTRIBUTION
# ============================================
echo "[1/7] Detecting Linux distribution..."

DISTRO="unknown"
PKG_MANAGER=""

if [ -f /etc/redhat-release ]; then
    DISTRO="rhel"
    # Check for dnf first (modern), fallback to yum (older)
    if command -v dnf &>/dev/null; then
        PKG_MANAGER="dnf"
    elif command -v yum &>/dev/null; then
        PKG_MANAGER="yum"
    fi
    DISTRO_NAME=$(cat /etc/redhat-release)
    echo "     [OK] Detected: $DISTRO_NAME"
    echo "     [OK] Package manager: $PKG_MANAGER"
elif [ -f /etc/debian_version ]; then
    DISTRO="debian"
    PKG_MANAGER="apt"
    if [ -f /etc/lsb-release ]; then
        DISTRO_NAME=$(grep DISTRIB_DESCRIPTION /etc/lsb-release | cut -d'"' -f2)
    else
        DISTRO_NAME="Debian $(cat /etc/debian_version)"
    fi
    echo "     [OK] Detected: $DISTRO_NAME"
    echo "     [OK] Package manager: apt"
elif [ -f /etc/os-release ]; then
    DISTRO_NAME=$(grep PRETTY_NAME /etc/os-release | cut -d'"' -f2)
    echo "     [WARN] Detected: $DISTRO_NAME"
    echo "     [WARN] Unknown distribution - will try generic approach"
else
    echo "     [WARN] Could not detect distribution"
    echo "     [WARN] Will try generic approach"
fi
echo ""

# ============================================
# STEP 2: CHECK/INSTALL PYTHON (3.10-3.12)
# ============================================
echo "[2/7] Checking Python installation..."
echo "     [INFO] Looking for Python 3.10, 3.11, or 3.12"
echo ""

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
    echo "     [WARN] Python 3.10-3.12 not found!"
    echo ""
    
    if [ "$DISTRO" = "rhel" ] && [ -n "$PKG_MANAGER" ]; then
        echo "     Attempting to install Python 3.11..."
        echo "     (You may be prompted for sudo password)"
        echo ""
        
        if sudo $PKG_MANAGER install -y python3.11 python3.11-pip python3.11-devel 2>&1; then
            PYTHON_CMD="python3.11"
            echo ""
            echo "     [OK] Python 3.11 installed successfully"
        else
            echo ""
            echo "     [ERROR] Failed to install Python automatically!"
            echo ""
            echo "     Please install manually:"
            echo "       sudo $PKG_MANAGER install python3.11 python3.11-pip python3.11-devel"
            echo ""
            read -p "Press Enter to exit..."
            exit 1
        fi
        
    elif [ "$DISTRO" = "debian" ]; then
        echo "     Attempting to install Python..."
        echo "     (You may be prompted for sudo password)"
        echo ""
        
        sudo apt update
        if sudo apt install -y python3 python3-venv python3-pip python3-dev 2>&1; then
            PYTHON_CMD="python3"
            echo ""
            echo "     [OK] Python installed successfully"
        else
            echo ""
            echo "     [ERROR] Failed to install Python automatically!"
            echo ""
            echo "     Please install manually:"
            echo "       sudo apt install python3 python3-venv python3-pip python3-dev"
            echo ""
            read -p "Press Enter to exit..."
            exit 1
        fi
        
    else
        echo "     [ERROR] Cannot auto-install Python on this system"
        echo ""
        echo "     Please install Python 3.10-3.12 manually:"
        echo "       - Red Hat/CentOS/Fedora: sudo dnf install python3.11 python3.11-pip python3.11-devel"
        echo "       - Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip"
        echo "       - Or download from: https://python.org/downloads/"
        echo ""
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo "     [OK] $PYTHON_VERSION - Compatible!"
echo "     [OK] Using command: $PYTHON_CMD"
echo ""

# ============================================
# STEP 3: CREATE VIRTUAL ENVIRONMENT
# ============================================
echo "[3/7] Setting up virtual environment..."
echo "     [INFO] Virtual environments isolate project dependencies"
echo ""

VENV_DIR="venv"

# Check if venv module is available
if ! $PYTHON_CMD -c "import venv" 2>/dev/null; then
    echo "     [WARN] venv module not available, attempting to install..."
    
    if [ "$DISTRO" = "rhel" ] && [ -n "$PKG_MANAGER" ]; then
        sudo $PKG_MANAGER install -y python3-devel 2>/dev/null || true
    elif [ "$DISTRO" = "debian" ]; then
        sudo apt install -y python3-venv python3-full 2>/dev/null || true
    fi
    
    # Check again
    if ! $PYTHON_CMD -c "import venv" 2>/dev/null; then
        echo "     [ERROR] Could not install venv module!"
        echo ""
        echo "     Please install manually:"
        if [ "$DISTRO" = "rhel" ]; then
            echo "       sudo $PKG_MANAGER install python3.11-devel"
        else
            echo "       sudo apt install python3-venv python3-full"
        fi
        echo ""
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

# Remove broken venv if it exists
if [ -d "$VENV_DIR" ] && [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "     [WARN] Found broken virtual environment, removing..."
    rm -rf "$VENV_DIR"
fi

# Create venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "     Creating virtual environment..."
    echo "     (This may take a moment...)"
    
    $PYTHON_CMD -m venv "$VENV_DIR" || {
        echo ""
        echo "     [ERROR] Failed to create virtual environment!"
        echo ""
        if [ "$DISTRO" = "rhel" ]; then
            echo "     Try: sudo $PKG_MANAGER install python3.11-devel"
        elif [ "$DISTRO" = "debian" ]; then
            echo "     Try: sudo apt install python3-venv python3-full"
        fi
        echo ""
        read -p "Press Enter to exit..."
        exit 1
    }
    
    echo "     [OK] Virtual environment created"
else
    echo "     [OK] Virtual environment already exists"
fi

# Activate virtual environment
echo "     Activating virtual environment..."

# Temporarily disable exit on error for source command
set +e
source "$VENV_DIR/bin/activate"
ACTIVATE_RESULT=$?
set -e

if [ $ACTIVATE_RESULT -ne 0 ] || [ -z "$VIRTUAL_ENV" ]; then
    echo "     [ERROR] Failed to activate virtual environment!"
    echo ""
    echo "     Try removing the venv folder and running again:"
    echo "       rm -rf venv"
    echo "       ./First_time_MultiModel.sh"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "     [OK] Activated: $VIRTUAL_ENV"
echo ""

# ============================================
# STEP 4: INSTALL PYTHON DEPENDENCIES
# ============================================
echo "[4/7] Installing Python dependencies..."
echo "     This may take 2-5 minutes on first run..."
echo ""

# Upgrade pip first (use public PyPI with proxy)
echo "     Upgrading pip..."
pip install --upgrade pip setuptools wheel --quiet --index-url https://pypi.org/simple/ --trusted-host pypi.org --trusted-host files.pythonhosted.org 2>/dev/null || pip install --upgrade pip setuptools wheel --index-url https://pypi.org/simple/ --trusted-host pypi.org --trusted-host files.pythonhosted.org

# Set pip to use public PyPI (through proxy)
PIP_INDEX="--index-url https://pypi.org/simple/ --trusted-host pypi.org --trusted-host files.pythonhosted.org"

# Install requirements (skip Windows-only packages)
echo "     Installing requirements.txt..."
if [ -f "requirements.txt" ]; then
    # Filter out pywin32 (Windows-only) and install
    grep -v "pywin32" requirements.txt > /tmp/requirements_linux.txt 2>/dev/null || cp requirements.txt /tmp/requirements_linux.txt
    
    pip install -r /tmp/requirements_linux.txt --quiet $PIP_INDEX 2>/dev/null || {
        echo "     [WARN] Some packages failed, trying essential ones individually..."
        pip install flask pandas numpy openpyxl scikit-learn --quiet $PIP_INDEX 2>/dev/null || true
    }
    
    rm -f /tmp/requirements_linux.txt
else
    echo "     [WARN] requirements.txt not found, installing essential packages..."
    pip install flask pandas numpy openpyxl scikit-learn requests tqdm --quiet $PIP_INDEX 2>/dev/null || true
fi

# Install LangChain (required for ChatGPT integration)
echo "     Installing LangChain..."
pip install "langchain>=0.1.0" "langchain-core>=0.1.0" "langchain-community>=0.3.0" --quiet $PIP_INDEX 2>/dev/null || {
    echo "     [WARN] LangChain install had issues, trying again..."
    pip install langchain langchain-core langchain-community $PIP_INDEX 2>/dev/null || true
}

# Install ChromaDB (vector store)
echo "     Installing ChromaDB..."
pip install chromadb --quiet $PIP_INDEX 2>/dev/null || pip install chromadb $PIP_INDEX || true

# Install sentence-transformers (embeddings) - pinned version for stability
echo "     Installing sentence-transformers..."
pip install sentence-transformers==2.2.2 --quiet $PIP_INDEX 2>/dev/null || pip install sentence-transformers==2.2.2 $PIP_INDEX || true

# Install O365 (Microsoft Graph API for Outlook email fetching)
echo "     Installing O365 (Microsoft Graph API)..."
pip install O365 --quiet $PIP_INDEX 2>/dev/null || pip install O365 $PIP_INDEX || true

# Install pysqlite3-binary (fix for old SQLite on RHEL)
echo "     Installing pysqlite3-binary (SQLite fix)..."
pip install pysqlite3-binary --quiet $PIP_INDEX 2>/dev/null || pip install pysqlite3-binary $PIP_INDEX || true

# Create SQLite fix file in app directory
echo "     Creating SQLite fix..."
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

# Add sqlite_fix import to sr_feedback_app.py if not already present
if ! grep -q "import sqlite_fix" app/sr_feedback_app.py 2>/dev/null; then
    sed -i '1i import sqlite_fix  # Fix for old SQLite on RHEL' app/sr_feedback_app.py
fi

echo ""
echo "     [OK] All dependencies installed"
echo ""

# ============================================
# STEP 5: VERIFY DEPENDENCIES
# ============================================
echo "[5/7] Verifying dependencies..."
echo ""

# SQLite fix for verification (apply before importing chromadb)
SQLITE_FIX="import sys; exec('try:\\n    __import__(\"pysqlite3\")\\n    sys.modules[\"sqlite3\"] = sys.modules.pop(\"pysqlite3\")\\nexcept: pass')"

# Use python from venv (not $PYTHON_CMD)
python -c "import flask; print('     [OK] flask', flask.__version__)" 2>/dev/null || echo "     [FAIL] flask not installed"
python -c "import pandas; print('     [OK] pandas', pandas.__version__)" 2>/dev/null || echo "     [FAIL] pandas not installed"
python -c "import numpy; print('     [OK] numpy', numpy.__version__)" 2>/dev/null || echo "     [FAIL] numpy not installed"
python -c "import openpyxl; print('     [OK] openpyxl', openpyxl.__version__)" 2>/dev/null || echo "     [FAIL] openpyxl not installed"
python -c "import langchain; print('     [OK] langchain', langchain.__version__)" 2>/dev/null || echo "     [WARN] langchain not installed"
python -c "$SQLITE_FIX; import chromadb; print('     [OK] chromadb', chromadb.__version__)" 2>/dev/null || echo "     [WARN] chromadb not installed"
python -c "import sentence_transformers; print('     [OK] sentence_transformers')" 2>/dev/null || echo "     [WARN] sentence_transformers not installed"

echo ""

# ============================================
# STEP 6: CHECK TOKENS AND DATABASES
# ============================================
echo "[6/7] Checking tokens and databases..."
echo ""

# Check tokens file
if [ -f "tokens/Tokens.xlsx" ]; then
    python -c "import pandas as pd; df = pd.read_excel('tokens/Tokens.xlsx'); print('     [OK] API tokens:', len(df), 'loaded')" 2>/dev/null || echo "     [WARN] Cannot read Tokens.xlsx"
else
    echo "     [ERROR] tokens/Tokens.xlsx NOT FOUND!"
    echo ""
    echo "     ================================================================"
    echo "      API TOKENS REQUIRED"
    echo "     ================================================================"
    echo "      Please create tokens/Tokens.xlsx with columns:"
    echo "        - Name or email: user@amdocs.com"
    echo "        - Token: your-api-token-here"
    echo ""
    echo "      Each token has \$4/day limit. Multiple tokens enable rotation."
    echo "     ================================================================"
fi

echo ""

# Check databases
DB_DIR="data/database"
VS_DIR="data/vectorstore"

if [ -d "$VS_DIR/chromadb_store" ]; then
    echo "     [OK] ChromaDB vectorstore found"
else
    echo "     [WARN] ChromaDB vectorstore not found - semantic search may not work"
fi

if [ -f "$DB_DIR/abbreviation.db" ]; then
    echo "     [OK] abbreviation.db"
else
    echo "     [WARN] abbreviation.db not found"
fi

if [ -f "$DB_DIR/people_skills.db" ]; then
    echo "     [OK] people_skills.db"
else
    echo "     [WARN] people_skills.db not found"
fi

if [ -f "$DB_DIR/sr_tracking.db" ]; then
    echo "     [OK] sr_tracking.db"
else
    echo "     [WARN] sr_tracking.db not found"
fi

if [ -f "$DB_DIR/workaround_feedback.db" ]; then
    echo "     [OK] workaround_feedback.db"
else
    echo "     [WARN] workaround_feedback.db not found"
fi

echo ""

# Check/Create SSL certificates for HTTPS
echo "     Checking SSL certificates..."
if [ -f "ssl/cert.pem" ] && [ -f "ssl/key.pem" ]; then
    echo "     [OK] SSL certificates found"
else
    echo "     [INFO] Creating self-signed SSL certificate for HTTPS..."
    mkdir -p ssl
    SERVER_HOSTNAME=$(hostname -f 2>/dev/null || hostname)
    openssl req -x509 -newkey rsa:2048 -nodes \
        -out ssl/cert.pem -keyout ssl/key.pem -days 365 \
        -subj "/C=US/ST=State/L=City/O=Amdocs/CN=${SERVER_HOSTNAME}" 2>/dev/null
    if [ -f "ssl/cert.pem" ]; then
        echo "     [OK] SSL certificate created for: ${SERVER_HOSTNAME}"
    else
        echo "     [WARN] Could not create SSL certificate - will run on HTTP"
    fi
fi

echo ""

# Test pipeline import
echo "     Testing Multi-Model pipeline import..."
python -c "
import sys
sys.path.insert(0, 'RAG/pipeline')
$SQLITE_FIX
try:
    from multi_model_rag_pipeline_chatgpt import MultiModelSRPipeline
    print('     [OK] Multi-Model pipeline ready')
except ImportError as e:
    print('     [WARN] Pipeline import failed:', str(e)[:50])
" 2>/dev/null || echo "     [WARN] Pipeline import check failed"

echo ""

# ============================================
# STEP 7: START APPLICATION
# ============================================
echo "[7/7] Setup complete!"
echo ""
echo "================================================================================"
echo "                       SETUP COMPLETE - STARTING APPLICATION"
echo "================================================================================"
echo ""
echo " ENVIRONMENT INFO:"
echo "  - Python: $PYTHON_VERSION"
echo "  - Virtual Env: $VENV_DIR"
echo "  - Working Directory: $(pwd)"
echo "  - Pipeline: MULTI-MODEL RAG (4 LLM Calls)"
echo ""
echo "================================================================================"
echo " MULTI-MODEL ARCHITECTURE:"
echo "================================================================================"
echo ""
echo "  LLM Call 1: Find Semantic Workaround"
echo "  LLM Call 2: Java Error Detection (5-Source Voting)"
echo "  LLM Call 3: Activity Name Extraction"
echo "  LLM Call 4: Final Resolution (Java or General)"
echo ""
echo "================================================================================"
echo " ACCESS PORTALS:"
echo "================================================================================"
echo ""
echo " USER PORTAL:  http://localhost:5000"
echo "   - Search SRs and view AI-generated workarounds"
echo "   - Vote on workarounds (thumbs up/down)"
echo "   - Provide feedback and corrections"
echo ""
echo " ADMIN PORTAL: http://localhost:5000/admin"
echo "   - Username: admin | Password: admin123"
echo "   - Upload Excel files for batch processing"
echo "   - View system statistics"
echo ""
echo "================================================================================"
echo " NOTES:"
echo "================================================================================"
echo "  * Each token has \$4/day limit - auto-rotates when exhausted"
echo "  * Processing time: ~15-30 seconds per SR"
echo "  * Press Ctrl+C to stop the Flask server"
echo ""
echo "================================================================================"
echo ""

echo "Starting Flask application..."
echo ""

# Start Flask (allow it to exit without triggering error trap)
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
read -p "Press Enter to exit..."
