import requests
import json
import time

URL = "http://localhost:8000/v1/generate_dragon"

def generate(filename, text, lang="ja", speed=1.0, intensity=1.0):
    payload = {
        "text": text,
        "language": lang,
        "speed": speed,
        "intensity": intensity
    }
    print(f"Generating '{filename}' with speed={speed}, intensity={intensity}...")
    try:
        start_time = time.time()
        response = requests.post(URL, json=payload)
        response.raise_for_status()
        
        with open(filename, "wb") as f:
            f.write(response.content)
        
        elapsed = time.time() - start_time
        print(f"Success! Saved to {filename} ({elapsed:.2f}s)")
    except Exception as e:
        print(f"Failed to generate {filename}: {e}")

text = "我は炎、我は死なり。"

# 1. Normal (Baseline)
generate("dragon_normal.wav", text, speed=1.0, intensity=1.0)

# 2. Fast Speed
generate("dragon_fast.wav", text, speed=1.5, intensity=1.0)

# 3. Slow Speed
generate("dragon_slow.wav", text, speed=0.7, intensity=1.0)

# 4. High Intensity (Deep & Distorted)
generate("dragon_intense.wav", text, speed=1.0, intensity=1.5)

# 5. Low Intensity (Mild)
generate("dragon_mild.wav", text, speed=1.0, intensity=0.5)
