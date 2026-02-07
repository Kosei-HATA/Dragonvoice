import requests
import json
import time

URL = "http://localhost:8000/v1/generate_dragon"

def generate(filename, text, lang="ja", speed=1.0, intensity=1.0, style="neutral"):
    payload = {
        "text": text,
        "language": lang,
        "speed": speed,
        "intensity": intensity,
        "style": style
    }
    print(f"Generating '{filename}' with style={style}, speed={speed}, intensity={intensity}...")
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

# 1. Neutral (Baseline)
generate("dragon_style_neutral.wav", text, style="neutral")

# 2. Angry (Aggressive, faster, more distorted)
generate("dragon_style_angry.wav", text, style="angry")

# 3. Dignified (Majestic, slower, deeper, clearer)
generate("dragon_style_dignified.wav", text, style="dignified")
