import requests
import json
import time

URL = "http://localhost:8000/v1/generate_dragon"
OUTPUT_FILE = "dragon_output.wav"

payload = {
    "text": "吾輩はドラゴンである。名前はまだない。どこで生まれたかとんと見当がつかぬ。",
    "language": "ja"
}

print(f"Sending request to {URL}...")
print(f"Payload: {json.dumps(payload, ensure_ascii=False)}")

start_time = time.time()
try:
    response = requests.post(URL, json=payload)
    response.raise_for_status()
    
    with open(OUTPUT_FILE, "wb") as f:
        f.write(response.content)
        
    elapsed = time.time() - start_time
    print(f"\nSuccess! Audio saved to '{OUTPUT_FILE}'")
    print(f"Time taken: {elapsed:.2f} seconds")
    
except requests.exceptions.ConnectionError:
    print("\nError: Could not connect to the server. Is it running?")
    print("Run: /opt/homebrew/anaconda3/envs/dragonvoice/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
except Exception as e:
    print(f"\nError: {e}")
