import torch
# Monkeypatch torch.load to default weights_only=False for TTS compatibility
# This is necessary because Coqui TTS uses older pickling that is blocked by PyTorch 2.6+ security defaults.
_original_load = torch.load
def safe_load(*args, **kwargs):
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return _original_load(*args, **kwargs)
torch.load = safe_load

from TTS.api import TTS
from app.config import Config
import os


class DragonTTS:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DragonTTS, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        print(f"Loading TTS model: {Config.TTS_MODEL_NAME} on {Config.DEVICE}")
        # Initialize TTS with the model name. 
        # specific args might be needed depending on the version, but standard API is clean.
        self.tts = TTS(Config.TTS_MODEL_NAME).to(Config.DEVICE)
        self.sample_rate = 24000 # XTTS v2 default

    def generate_raw_audio(self, text: str, language: str, speed: float = 1.0, temperature: float = 0.75):
        """
        Generates raw audio data (list of floats) from text.
        temperature: Controls generation randomness. Higher = unstable/emotional. Lower = stable.
        """
        if not os.path.exists(Config.SAMPLING_AUDIO_PATH):
            raise FileNotFoundError(f"Sampling audio not found at {Config.SAMPLING_AUDIO_PATH}")

        with torch.no_grad():
            # tts() returns a list of float values representing the waveform
            wav = self.tts.tts(
                text=text,
                speaker_wav=Config.SAMPLING_AUDIO_PATH,
                language=language,
                speed=speed,
                temperature=temperature
            )
        return wav, self.sample_rate

tts_service = DragonTTS()
