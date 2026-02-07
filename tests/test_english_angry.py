import requests
import json
import time

URL = "http://localhost:8000/v1/generate_dragon"

def generate(filename, text, lang="en", speed=1.0, intensity=1.0, style="neutral", reverb=1.0):
    payload = {
        "text": text,
        "language": lang,
        "speed": speed,
        "intensity": intensity,
        "style": style,
        "reverb": reverb
    }
    print(f"Generating '{filename}'...")
    print(f"Params: Style={style}, Speed={speed}, Intensity={intensity}, Reverb={reverb}, Lang={lang}")
    
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
        if hasattr(e, 'response') and e.response is not None:
            print(e.response.text)

# Text: "I am the dragon. Fire consumes all!"
text = "I am the dragon. Fire consumes all!"

# Parameters requested:
# - Angry High -> Style="angry", Intensity=1.5
# - Slow -> Speed=0.7
# - Low Reverb -> Reverb=0.3
generate(
    "dragon_english_angry_slow_dry.wav", 
    text, 
    lang="en", 
    speed=0.7, 
    intensity=1.5, 
    style="angry", 
    reverb=0.3
)
