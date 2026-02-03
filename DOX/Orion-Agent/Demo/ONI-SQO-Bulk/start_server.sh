#!/bin/bash
# ONI-SQO-Bulk Console - Linux Server Startup Script

echo "============================================================"
echo "       ONI-SQO-Bulk Console - Server Deployment"
echo "============================================================"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Get server IP
SERVER_IP=$(hostname -I | awk '{print $1}')

echo ""
echo "Server IP: $SERVER_IP"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found!"
    echo "Install with: sudo apt install python3 python3-pip"
    exit 1
fi

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "[1/4] Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "[2/4] Installing dependencies..."
pip install -q -r requirements.txt

# Kill existing processes on ports
echo "[3/4] Cleaning up old processes..."
fuser -k 5003/tcp 2>/dev/null
fuser -k 8080/tcp 2>/dev/null
sleep 1

# Start Backend
echo "[4/4] Starting servers..."
cd backend
nohup python app.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Start Frontend
nohup python -m http.server 8080 --bind 0.0.0.0 > logs/frontend.log 2>&1 &
FRONTEND_PID=$!

# Create logs directory if not exists
mkdir -p logs

# Save PIDs for later shutdown
echo "$BACKEND_PID" > logs/backend.pid
echo "$FRONTEND_PID" > logs/frontend.pid

sleep 2

echo ""
echo "============================================================"
echo "           SERVERS STARTED SUCCESSFULLY!"
echo "============================================================"
echo ""
echo "   Backend PID:  $BACKEND_PID"
echo "   Frontend PID: $FRONTEND_PID"
echo ""
echo "   ACCESS URLs:"
echo "     Local:   http://localhost:8080"
echo "     Network: http://$SERVER_IP:8080"
echo ""
echo "   LOGS:"
echo "     Backend:  logs/backend.log"
echo "     Frontend: logs/frontend.log"
echo ""
echo "   TO STOP SERVERS:"
echo "     ./stop_server.sh"
echo "     OR: kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "============================================================"
