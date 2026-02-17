#!/bin/bash
# Moovy Application Launcher for macOS and Linux
# This script sets up the virtual environment and launches the Moovy application

echo ""
echo "========================================"
echo "  Moovy - Movie Codec Analyzer"
echo "========================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo ""
    echo "Please install Python 3:"
    echo "  macOS:  brew install python3"
    echo "  Linux:  sudo apt-get install python3 python3-venv (Ubuntu/Debian)"
    echo "          sudo dnf install python3 (Fedora)"
    echo "          sudo pacman -S python (Arch)"
    echo ""
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Setting up Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install/upgrade pip
pip install --upgrade pip setuptools wheel > /dev/null 2>&1

# Install requirements
echo "Installing/updating dependencies..."
pip install -q -r requirements.txt

# Check for FFmpeg
echo ""
echo "Checking for FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    echo "✓ FFmpeg found!"
else
    echo ""
    echo "⚠️  WARNING: FFmpeg not found!"
    echo ""
    echo "To use Moovy, you need to install FFmpeg:"
    echo ""
    echo "macOS:"
    echo "  brew install ffmpeg"
    echo ""
    echo "Linux (Ubuntu/Debian):"
    echo "  sudo apt-get install ffmpeg"
    echo ""
    echo "Linux (Fedora):"
    echo "  sudo dnf install ffmpeg"
    echo ""
    echo "Linux (Arch):"
    echo "  sudo pacman -S ffmpeg"
    echo ""
fi

# Launch the application
echo ""
echo "Launching Moovy..."
python -m src.main

# Deactivate virtual environment on exit
deactivate
