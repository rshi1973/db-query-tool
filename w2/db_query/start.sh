#!/bin/bash
# Start script for Database Query Tool
# Starts both backend and frontend servers

set -e

# Colors for output
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting Database Query Tool...${NC}"
echo ""

# Check if backend .env exists
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}Warning: backend/.env not found${NC}"
    echo "Creating from .env.example..."
    if [ -f "backend/.env.example" ]; then
        cp backend/.env.example backend/.env
        echo -e "${YELLOW}Please edit backend/.env and add your GEMINI_API_KEY${NC}"
    else
        echo -e "${YELLOW}backend/.env.example not found. Please create backend/.env manually.${NC}"
    fi
    echo ""
fi

# Function to cleanup background processes on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Shutting down servers...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit
}

trap cleanup INT TERM

# Start backend
echo -e "${GREEN}Starting backend server on http://localhost:8000${NC}"
cd backend
if command -v uv &> /dev/null; then
    uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
else
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
fi
BACKEND_PID=$!
cd ..

# Wait a bit for backend to start
sleep 2

# Start frontend
echo -e "${GREEN}Starting frontend server on http://localhost:5173${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo -e "${GREEN}✓ Servers started!${NC}"
echo ""
echo "Backend API:  http://localhost:8000"
echo "Backend Docs: http://localhost:8000/docs"
echo "Frontend:     http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for both processes
wait

