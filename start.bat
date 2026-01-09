@echo off
REM Startup script for Resonance Without Sound (Windows)
REM This script starts both backend and frontend servers

echo 🎵 Starting Resonance Without Sound...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.9+ first.
    exit /b 1
)

REM Check if Node is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found. Please install Node.js 16+ first.
    exit /b 1
)

REM Start backend
echo 🔧 Starting backend server...
cd backend

REM Check if venv exists
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate venv and install dependencies
call venv\Scripts\activate.bat
pip install -q -r requirements.txt

REM Check for .env file
if not exist ".env" (
    echo ⚠️  Warning: .env file not found. Copying from .env.example...
    copy .env.example .env
    echo ⚠️  Please edit backend\.env and add your OPENAI_API_KEY
    echo.
)

REM Start backend in new window
echo ✅ Backend starting on http://localhost:8000
start "Resonance Backend" cmd /k python main.py

cd ..

REM Start frontend
echo 🎨 Starting frontend server...
cd frontend

REM Install dependencies if needed
if not exist "node_modules" (
    echo Installing Node dependencies...
    call npm install
)

echo ✅ Frontend starting on http://localhost:3000
start "Resonance Frontend" cmd /k npm start

cd ..

echo.
echo 🎉 Resonance Without Sound is running!
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Two new windows have opened for backend and frontend servers.
echo Close those windows to stop the servers.
echo.
pause
