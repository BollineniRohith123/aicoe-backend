#!/bin/bash

# AICOE Platform Status Check Script
# This script checks the status of both backend and frontend servers

echo "🔍 AICOE Platform Status Check"
echo "================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if a port is in use
check_port() {
    lsof -i :$1 > /dev/null 2>&1
    return $?
}

# Function to get PID on port
get_pid_on_port() {
    lsof -ti :$1 2>/dev/null
}

# Function to check HTTP endpoint
check_http() {
    curl -s -o /dev/null -w "%{http_code}" --connect-timeout 2 "$1"
}

# Check Backend
echo -e "${BLUE}🔧 Backend Server (Port 8000)${NC}"
echo "----------------------------"
if check_port 8000; then
    PID=$(get_pid_on_port 8000)
    echo -e "Status: ${GREEN}✅ RUNNING${NC}"
    echo "PID: $PID"

    # Check if API is responding
    HTTP_CODE=$(check_http "http://localhost:8000/health")
    if [ "$HTTP_CODE" = "200" ]; then
        echo -e "Health Check: ${GREEN}✅ HEALTHY${NC}"
    else
        echo -e "Health Check: ${YELLOW}⚠️  UNHEALTHY (HTTP $HTTP_CODE)${NC}"
    fi

    echo "URL: http://localhost:8000"
    echo "API Docs: http://localhost:8000/docs"

    if [ -f "logs/backend.log" ]; then
        echo "Log file: logs/backend.log"
        echo "Recent logs:"
        tail -n 3 logs/backend.log | sed 's/^/  /'
    fi
else
    echo -e "Status: ${RED}❌ NOT RUNNING${NC}"
fi

echo ""

# Check Frontend
echo -e "${BLUE}⚛️  Frontend Server (Port 3000)${NC}"
echo "----------------------------"
if check_port 3000; then
    PID=$(get_pid_on_port 3000)
    echo -e "Status: ${GREEN}✅ RUNNING${NC}"
    echo "PID: $PID"

    # Check if frontend is responding
    HTTP_CODE=$(check_http "http://localhost:3000")
    if [ "$HTTP_CODE" = "200" ]; then
        echo -e "Health Check: ${GREEN}✅ HEALTHY${NC}"
    else
        echo -e "Health Check: ${YELLOW}⚠️  LOADING (HTTP $HTTP_CODE)${NC}"
    fi

    echo "URL: http://localhost:3000"

    if [ -f "logs/frontend.log" ]; then
        echo "Log file: logs/frontend.log"
        echo "Recent logs:"
        tail -n 3 logs/frontend.log | sed 's/^/  /'
    fi
else
    echo -e "Status: ${RED}❌ NOT RUNNING${NC}"
fi

echo ""
echo "================================"

# Summary
BACKEND_RUNNING=0
FRONTEND_RUNNING=0

check_port 8000 && BACKEND_RUNNING=1
check_port 3000 && FRONTEND_RUNNING=1

if [ $BACKEND_RUNNING -eq 1 ] && [ $FRONTEND_RUNNING -eq 1 ]; then
    echo -e "${GREEN}✅ All systems operational!${NC}"
elif [ $BACKEND_RUNNING -eq 1 ] || [ $FRONTEND_RUNNING -eq 1 ]; then
    echo -e "${YELLOW}⚠️  Partial system running${NC}"
else
    echo -e "${RED}❌ No servers running${NC}"
    echo ""
    echo "💡 To start the servers, run: ./start.sh"
fi

echo ""
echo "📊 Available commands:"
echo "   ./start.sh  - Start all servers"
echo "   ./stop.sh   - Stop all servers"
echo "   ./status.sh - Check server status"
echo ""
