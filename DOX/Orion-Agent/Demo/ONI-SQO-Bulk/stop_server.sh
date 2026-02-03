#!/bin/bash
# ONI-SQO-Bulk Console - Stop Server Script

echo "Stopping ONI-SQO-Bulk servers..."

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Kill using saved PIDs
if [ -f "logs/backend.pid" ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    kill $BACKEND_PID 2>/dev/null && echo "Backend stopped (PID: $BACKEND_PID)"
    rm logs/backend.pid
fi

if [ -f "logs/frontend.pid" ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    kill $FRONTEND_PID 2>/dev/null && echo "Frontend stopped (PID: $FRONTEND_PID)"
    rm logs/frontend.pid
fi

# Also kill any processes on the ports (in case PIDs don't match)
fuser -k 5003/tcp 2>/dev/null
fuser -k 8080/tcp 2>/dev/null

echo "All servers stopped."
