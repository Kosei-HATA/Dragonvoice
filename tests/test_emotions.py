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

text = "貴様ぁ！　我が眠りを妨げる者は、誰だぁ！"

# 1. Angry (Base) - Should have mild bitcrush and high temperature
generate("dragon_emotion_angry_base.wav", text, style="angry", intensity=1.0)

# 2. Angry (High Intensity) - Should have heavy bitcrush and higher temperature (unstable)
generate("dragon_emotion_angry_high.wav", text, style="angry", intensity=1.5)

# 3. Dignified (Control) - Should be clean and stable
generate("dragon_emotion_dignified.wav", text, style="dignified", intensity=1.0)
