import requests
import json
import time

URL = "http://localhost:8000/v1/generate_dragon"

def generate(filename, text, lang="ja", speed=1.0, intensity=1.0, style="neutral", reverb=1.0):
    payload = {
        "text": text,
        "language": lang,
        "speed": speed,
        "intensity": intensity,
        "style": style,
        "reverb": reverb
    }
    print(f"Generating '{filename}' with style={style}, reverb={reverb}...")
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

text = "響け、我が声よ！"

# 1. Neutral Base (Reverb 1.0)
generate("dragon_reverb_normal.wav", text, style="neutral", reverb=1.0)

# 2. Dry (No Reverb)
generate("dragon_reverb_dry.wav", text, style="neutral", reverb=0.0)

# 3. Wet (Heavy Reverb)
generate("dragon_reverb_wet.wav", text, style="neutral", reverb=2.0)
