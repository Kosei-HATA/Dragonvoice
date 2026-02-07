#!/bin/bash

# Dragon Voice Installation Script for macOS/Linux

echo "🐉 Dragon Voice Installer (macOS/Linux) 🐉"
echo "=========================================="

# 1. Check for Python 3.10+
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 could not be found."
    echo "Please install Python 3.10 or higher from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
REQUIRED_VERSION="3.10"

if [[ $(echo -e "$PYTHON_VERSION\n$REQUIRED_VERSION" | sort -V | head -n1) != "$REQUIRED_VERSION" ]]; then
     echo "❌ Python 3.10+ is required. Found version $PYTHON_VERSION"
     exit 1
fi

echo "✅ Python $PYTHON_VERSION found."

# 2. Check for FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg is not installed!"
    echo "It is highly recommended for audio processing."
    echo "Install it via Homebrew: brew install ffmpeg"
    # We won't exit, as some simple TTS might work, but warn strongly.
else
    echo "✅ FFmpeg found."
fi

# 3. Create Virtual Environment
VENV_NAME="venv_dragon"
if [ ! -d "$VENV_NAME" ]; then
    echo "📦 Creating virtual environment '$VENV_NAME'..."
    python3 -m venv $VENV_NAME
else
    echo "ℹ️  Virtual environment '$VENV_NAME' already exists."
fi

# 3. Activate and Install
echo "🔌 Activating virtual environment..."
source $VENV_NAME/bin/activate

echo "⬇️  Installing dependencies using pip..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Check for Sampling Audio
if [ ! -f "sampling_dialogue.wav" ]; then
    echo "⚠️  'sampling_dialogue.wav' not found!"
    echo "Please ensure you have a reference audio file named 'sampling_dialogue.wav' in this folder."
else
    echo "✅ 'sampling_dialogue.wav' found."
fi

echo ""
echo "🎉 Installation Complete!"
echo "=========================================="
echo "To start the Dragon Voice server, run:"
echo "  source $VENV_NAME/bin/activate"
echo "  python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
echo ""
