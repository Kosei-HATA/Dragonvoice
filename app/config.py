import os
from pathlib import Path
import torch

class Config:
    # Base Paths
    BASE_DIR = Path(__file__).resolve().parent.parent
    ASSETS_DIR = BASE_DIR
    
    # Audio Settings
    SAMPLING_AUDIO_FILENAME = "sampling_dialogue.wav"
    SAMPLING_AUDIO_PATH = os.path.join(ASSETS_DIR, SAMPLING_AUDIO_FILENAME)
    
    # Model Settings
    TTS_MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
    
    if torch.cuda.is_available():
        DEVICE = "cuda"
    elif torch.backends.mps.is_available():
        DEVICE = "mps"
    else:
        DEVICE = "cpu"
    
    # Dragon Effect Settings
    PITCH_SHIFT_SEMITONES = -6.0
    LOW_PASS_CUTOFF_HZ = 700
    DISTORTION_DRIVE_DB = 4.0
    REVERB_ROOM_SIZE = 0.8
    REVERB_WET_LEVEL = 0.35
    
    # API Settings
    API_HOST = "0.0.0.0"
    API_PORT = 8000

config = Config()
