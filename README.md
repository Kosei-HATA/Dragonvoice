# Dragon Voice API 🐉

A powerful Text-to-Speech (TTS) API that generates dragon-like voices using Coqui XTTS v2 and DSP effects (Pedalboard). It supports English, Japanese, and other languages, with adjustable parameters for speed, intensity, style, and reverb.

## Features

- **High-Quality Voice Cloning**: Uses Coqui XTTS v2 for realistic speech generation.
- **Dragon DSP Effects**: Applies pitch shifting, distortion, and reverb to create a monstrous voice.
- **Adjustable Parameters**:
    - `speed`: Speaking rate.
    - `intensity`: Power and distortion level.
    - `style`: "Neutral", "Angry" (shouting), or "Dignified" (deep/majestic).
    - `reverb`: Echo amount.
- **API Interface**: Simple REST API built with FastAPI.

## Requirements

- Python 3.10+
- macOS (Apple Silicon recommended) or Linux (NVIDIA GPU recommended)
- `ffmpeg` (for audio processing)

## Installation

## Installation

### Easy Method (Scripts)

**macOS / Linux:**
```bash
chmod +x install_mac.sh
./install_mac.sh
```

**Windows:**
Double-click `install_windows.bat` or run it from Command Prompt.

### Manual Method

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/dragonvoice.git
    cd dragonvoice
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Prepare Assets:**
    Ensure `sampling_dialogue.wav` (the reference voice sample) is in the root directory.

## Usage

1.  **Start the Server:**
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```

2.  **Open Swagger UI:**
    Go to [http://localhost:8000/docs](http://localhost:8000/docs) to test the API interactively.

3.  **Example Request (curl):**
    ```bash
    curl -X 'POST' \
      'http://localhost:8000/v1/generate_dragon' \
      -H 'Content-Type: application/json' \
      -d '{
        "text": "吾輩はドラゴンである。",
        "language": "ja",
        "speed": 1.0,
        "intensity": 1.5,
        "style": "dignified",
        "reverb": 1.2
      }' --output dragon.wav
    ```

## API Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `text` | string | (Required) | Text to speak. |
| `language` | string | `"en"` | Language code (e.g., `en`, `ja`). |
| `speed` | float | `1.0` | Speaking rate (0.5 - 2.0). |
| `intensity` | float | `1.0` | Vigor/Distortion level (0.0 - 2.0). |
| `style` | string | `"neutral"` | Preset persona: `neutral`, `angry`, `dignified`. |
| `reverb` | float | `1.0` | Reverb amount (0.0 - 2.0). |

## Testing

Test scripts are located in the `tests/` directory:
- `python tests/test_api.py`: Basic generation test.
- `python tests/test_parameters.py`: Test speed/intensity variations.
- `python tests/test_styles.py`: Test styles (Angry/Dignified).
- `python tests/test_reverb.py`: Test reverb settings.

## License

MIT
