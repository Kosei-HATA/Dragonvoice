import torchaudio
import soundfile

print(f"Torchaudio version: {torchaudio.__version__}")
print(f"Soundfile version: {soundfile.__version__}")

try:
    print(f"Available backends: {torchaudio.list_audio_backends()}")
except Exception as e:
    print(f"list_audio_backends failed: {e}")

try:
    # Try to load the sample file
    print("Attempting to load sampling_dialogue.wav...")
    torchaudio.load("sampling_dialogue.wav")
    print("Success loading with default backend.")
except Exception as e:
    print(f"Failed loading with default backend: {e}")

try:
    # Try to load forcing soundfile
    print("Attempting to load with backend='soundfile'...")
    torchaudio.load("sampling_dialogue.wav", backend="soundfile")
    print("Success loading with soundfile backend.")
except Exception as e:
    print(f"Failed loading with soundfile backend: {e}")
