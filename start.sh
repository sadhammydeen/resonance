#!/bin/bash

# Startup script for Resonance Without Sound
# This script starts both backend and frontend servers

echo "🎵 Starting Resonance Without Sound..."
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null
then
    echo "❌ Python not found. Please install Python 3.9+ first."
    exit 1
fi

# Check if Node is installed
if ! command -v node &> /dev/null
then
    echo "❌ Node.js not found. Please install Node.js 16+ first."
    exit 1
fi

# Start backend
echo "🔧 Starting backend server..."
cd backend

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv venv
fi

# Activate venv and install dependencies
source venv/bin/activate
pip install -q -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env and add your OPENAI_API_KEY"
fi

# Start backend in background
echo "✅ Backend starting on http://localhost:8000"
python main.py &
BACKEND_PID=$!

cd ..

# Start frontend
echo "🎨 Starting frontend server..."
cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install
fi

echo "✅ Frontend starting on http://localhost:3000"
npm start &
FRONTEND_PID=$!

cd ..

echo ""
echo "🎉 Resonance Without Sound is running!"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
