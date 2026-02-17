@echo off
REM Moovy Application Launcher
REM This script sets up the virtual environment and launches the Moovy application

echo.
echo ========================================
echo  Moovy - Movie Codec Analyzer
echo ========================================
echo.

REM Check if Python virtual environment exists
if not exist ".venv" (
    echo Setting up Python virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install requirements
echo Installing/updating dependencies...
pip install -q -r requirements.txt

REM Check for FFmpeg
echo.
echo Checking for FFmpeg...
where ffmpeg >nul 2>nul
if %errorlevel% equ 0 (
    echo ✓ FFmpeg found!
) else (
    echo.
    echo ⚠ WARNING: FFmpeg not found!
    echo.
    echo To use Moovy, you need to install FFmpeg.
    echo.
    echo Option 1: Download from https://ffmpeg.org/download.html
    echo Option 2: Run the setup_ffmpeg.ps1 script
    echo.
)

REM Launch the application
echo.
echo Launching Moovy...
python -m src.main

pause
