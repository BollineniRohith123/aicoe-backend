#!/bin/bash

# AICOE Platform Shutdown Script
# This script stops both the backend and frontend servers

echo "🛑 Stopping AICOE Platform..."
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to kill process on port
kill_port() {
    if lsof -i :$1 > /dev/null 2>&1; then
        echo "Stopping process on port $1..."
        lsof -ti :$1 | xargs kill -9 2>/dev/null
        return 0
    else
        echo "No process found on port $1"
        return 1
    fi
}

# Function to kill process by PID
kill_pid() {
    if [ -f "$1" ]; then
        PID=$(cat "$1")
        if ps -p $PID > /dev/null 2>&1; then
            echo "Killing process $PID..."
            kill -9 $PID 2>/dev/null
            rm "$1"
            return 0
        else
            echo "Process $PID not running"
            rm "$1"
            return 1
        fi
    fi
    return 1
}

STOPPED_SOMETHING=0

# Try to stop backend using PID file
if [ -f "logs/backend.pid" ]; then
    echo "🔧 Stopping Backend Server..."
    if kill_pid "logs/backend.pid"; then
        echo -e "${GREEN}✅ Backend server stopped${NC}"
        STOPPED_SOMETHING=1
    fi
else
    # Try to stop by port
    echo "🔧 Stopping Backend Server (by port)..."
    if kill_port 8000; then
        echo -e "${GREEN}✅ Backend server stopped${NC}"
        STOPPED_SOMETHING=1
    fi
fi

# Try to stop frontend using PID file
if [ -f "logs/frontend.pid" ]; then
    echo "⚛️  Stopping Frontend Server..."
    if kill_pid "logs/frontend.pid"; then
        echo -e "${GREEN}✅ Frontend server stopped${NC}"
        STOPPED_SOMETHING=1
    fi
else
    # Try to stop by port
    echo "⚛️  Stopping Frontend Server (by port)..."
    if kill_port 3000; then
        echo -e "${GREEN}✅ Frontend server stopped${NC}"
        STOPPED_SOMETHING=1
    fi
fi

# Additional cleanup - kill any remaining node/uvicorn processes
echo ""
echo "🧹 Cleaning up remaining processes..."

# Kill any remaining uvicorn processes
pkill -f "uvicorn server:app" 2>/dev/null && echo "Cleaned up uvicorn processes"

# Kill any remaining npm/react processes on port 3000
pkill -f "react-scripts start" 2>/dev/null && echo "Cleaned up React processes"

echo ""
if [ $STOPPED_SOMETHING -eq 1 ]; then
    echo "================================"
    echo -e "${GREEN}✅ AICOE Platform stopped successfully!${NC}"
    echo "================================"
else
    echo "================================"
    echo -e "${YELLOW}⚠️  No running servers found${NC}"
    echo "================================"
fi

echo ""
echo "💡 To start the servers again, run: ./start.sh"
echo ""
