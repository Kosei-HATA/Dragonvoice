@echo off
setlocal

echo "🐉 Dragon Voice Installer (Windows) 🐉"
echo "=========================================="

rem 1. Check for Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo "❌ Python is not installed or not in your PATH."
    echo "Please download and install Python 3.10+ from https://www.python.org/downloads/"
    echo "Ensure you check 'Add Python to PATH' during installation."
    pause
    exit /b 1
)

rem Check Version (rudimentary check, assumes 'python' works)
echo "✅ Python found."

rem 2. Check for FFmpeg
where ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
    echo "⚠️  FFmpeg is not found in your PATH!"
    echo "It is recommended for audio processing."
    echo "Please download from https://ffmpeg.org/download.html and add to PATH."
) else (
    echo "✅ FFmpeg found."
)

rem 3. Create Virtual Environment
set VENV_NAME=venv_dragon
if not exist "%VENV_NAME%" (
    echo "📦 Creating virtual environment '%VENV_NAME%'..."
    python -m venv %VENV_NAME%
) else (
    echo "ℹ️  Virtual environment '%VENV_NAME%' already exists."
)

rem 3. Activate and Install
echo "🔌 Activating virtual environment..."
call %VENV_NAME%\Scripts\activate

echo "⬇️  Installing dependencies using pip..."
pip install --upgrade pip
pip install -r requirements.txt

rem 4. Check for Sampling Audio
if not exist "sampling_dialogue.wav" (
    echo "⚠️  'sampling_dialogue.wav' not found!"
    echo "Please ensure you have a reference audio file named 'sampling_dialogue.wav' in this folder."
) else (
    echo "✅ 'sampling_dialogue.wav' found."
)

echo ""
echo "🎉 Installation Complete!"
echo "=========================================="
echo "To starting the Dragon Voice server, execute:"
echo "  %VENV_NAME%\Scripts\activate"
echo "  python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
echo ""
pause
