@echo off
REM Quick start script for backend (Windows)

echo ==========================================
echo AI-Based Lecture Summarizer - Backend
echo ==========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if FFmpeg is installed
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo Error: FFmpeg is not installed
    echo Please install FFmpeg from https://ffmpeg.org/download.html
    echo Or use: winget install ffmpeg
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Run the server
echo.
echo ==========================================
echo Starting backend server...
echo Server will run on: http://localhost:5000
echo ==========================================
echo.
python app.py

pause
