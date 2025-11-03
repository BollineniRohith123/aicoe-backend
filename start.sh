#!/bin/bash

# AICOE Platform Startup Script
# This script starts both the backend and frontend servers

echo "🚀 Starting AICOE Platform..."
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if a port is in use
check_port() {
    lsof -i :$1 > /dev/null 2>&1
    return $?
}

# Function to kill process on port
kill_port() {
    echo "Killing process on port $1..."
    lsof -ti :$1 | xargs kill -9 2>/dev/null
}

# Check if ports are already in use
if check_port 8000; then
    echo -e "${YELLOW}⚠️  Port 8000 is already in use${NC}"
    read -p "Do you want to kill the existing process? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        kill_port 8000
    else
        echo -e "${RED}❌ Cannot start backend on port 8000${NC}"
        exit 1
    fi
fi

if check_port 3000; then
    echo -e "${YELLOW}⚠️  Port 3000 is already in use${NC}"
    read -p "Do you want to kill the existing process? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        kill_port 3000
    else
        echo -e "${RED}❌ Cannot start frontend on port 3000${NC}"
        exit 1
    fi
fi

# Check if backend .env exists
if [ ! -f "backend/.env" ]; then
    echo -e "${RED}❌ backend/.env file not found!${NC}"
    echo "Please create backend/.env with your OPENROUTER_API_KEY"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating one...${NC}"
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
fi

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}⚠️  node_modules not found. Installing dependencies...${NC}"
    cd frontend
    npm install
    cd ..
fi

# Create log directory
mkdir -p logs

echo ""
echo "================================"
echo -e "${GREEN}✅ Pre-flight checks complete!${NC}"
echo "================================"
echo ""

# Start backend in background
echo "🔧 Starting Backend Server (Port 8000)..."
cd backend
source venv/bin/activate
nohup uvicorn server:app --host 0.0.0.0 --port 8000 --reload > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Check if backend started successfully
if check_port 8000; then
    echo -e "${GREEN}✅ Backend server started successfully (PID: $BACKEND_PID)${NC}"
    echo "   📊 Backend logs: tail -f logs/backend.log"
    echo "   🌐 Backend URL: http://localhost:8000"
    echo "   📚 API Docs: http://localhost:8000/docs"
else
    echo -e "${RED}❌ Failed to start backend server${NC}"
    echo "Check logs/backend.log for details"
    exit 1
fi

echo ""

# Start frontend in background
echo "⚛️  Starting Frontend Server (Port 3000)..."
cd frontend
nohup npm start > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
echo "⏳ Waiting for frontend to start (this may take 30-60 seconds)..."
COUNTER=0
MAX_WAIT=60
while [ $COUNTER -lt $MAX_WAIT ]; do
    if check_port 3000; then
        echo -e "${GREEN}✅ Frontend server started successfully (PID: $FRONTEND_PID)${NC}"
        echo "   📊 Frontend logs: tail -f logs/frontend.log"
        echo "   🌐 Frontend URL: http://localhost:3000"
        break
    fi
    sleep 2
    COUNTER=$((COUNTER + 2))
    echo -n "."
done

echo ""

if ! check_port 3000; then
    echo -e "${RED}❌ Frontend took too long to start${NC}"
    echo "Check logs/frontend.log for details"
    echo "Backend is still running on port 8000"
    exit 1
fi

# Save PIDs for later shutdown
echo "$BACKEND_PID" > logs/backend.pid
echo "$FRONTEND_PID" > logs/frontend.pid

echo ""
echo "================================"
echo -e "${GREEN}🎉 AICOE Platform is running!${NC}"
echo "================================"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "📊 View logs:"
echo "   Backend:  tail -f logs/backend.log"
echo "   Frontend: tail -f logs/frontend.log"
echo ""
echo "🛑 To stop the servers, run: ./stop.sh"
echo ""
echo -e "${YELLOW}💡 Tip: Open http://localhost:3000 in your browser to get started!${NC}"
echo ""

# Optional: Open browser automatically (uncomment if desired)
# sleep 5
# open http://localhost:3000
