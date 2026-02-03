#!/bin/bash
# ============================================
# Keep SR-Analyzer Server Alive
# Checks if the server is running and restarts if needed
# Add to crontab: */5 * * * * /path/to/keep_alive.sh >> /path/to/keep_alive.log 2>&1
# ============================================

APP_DIR="/ossusers1/oss/users/rke/sr-analyzer/semantic-resolution"
LOG_FILE="${APP_DIR}/logs/keep_alive.log"
PID_FILE="${APP_DIR}/server.pid"
PYTHON_SCRIPT="app/sr_feedback_app.py"
PORT=5000

# Create logs directory if not exists
mkdir -p "${APP_DIR}/logs"

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Check if server is running on the port
is_running() {
    if lsof -i:$PORT -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Check if server responds to health check
is_healthy() {
    response=$(curl -sk --max-time 10 "https://localhost:${PORT}/" 2>/dev/null)
    if [ $? -eq 0 ]; then
        return 0
    else
        return 1
    fi
}

# Start the server
start_server() {
    log "Starting server..."
    
    cd "$APP_DIR" || exit 1
    
    # Set up environment
    source venv/bin/activate
    
    # Set proxy (needed for some operations)
    export HTTP_PROXY=http://genproxy.corp.amdocs.com:8080/
    export HTTPS_PROXY=http://genproxy.corp.amdocs.com:8080/
    export no_proxy=localhost,127.0.0.1,.corp.amdocs.com,.amdocs.com,ai-framework1
    
    # Set Azure AD redirect URI
    SERVER_HOSTNAME=$(hostname -f 2>/dev/null || hostname)
    export AZURE_REDIRECT_URI="https://${SERVER_HOSTNAME}:5000/auth/microsoft/callback"
    
    # Start server in background with nohup
    nohup python "$PYTHON_SCRIPT" >> "${APP_DIR}/logs/server.log" 2>&1 &
    
    # Save PID
    echo $! > "$PID_FILE"
    
    log "Server started with PID: $(cat $PID_FILE)"
    
    # Wait a bit for server to start
    sleep 10
    
    if is_running; then
        log "Server is now running on port $PORT"
    else
        log "ERROR: Server failed to start!"
    fi
}

# Main logic
main() {
    if is_running; then
        # Server process exists, check if healthy
        if is_healthy; then
            # All good, exit silently (no log spam)
            exit 0
        else
            log "WARNING: Server process exists but not responding. Restarting..."
            # Kill existing process
            pkill -f "$PYTHON_SCRIPT" 2>/dev/null
            sleep 2
            start_server
        fi
    else
        log "Server not running. Starting..."
        start_server
    fi
}

main

