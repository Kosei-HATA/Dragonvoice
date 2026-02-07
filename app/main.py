from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from app.schemas import DragonRequest
from app.services.tts_service import tts_service
from app.services.dsp_service import dsp_service
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Dragon Voice TTS API", version="1.0.0")

@app.post("/v1/generate_dragon",
    responses={
        200: {
            "content": {"audio/wav": {}},
            "description": "Generated dragon voice audio file.",
        }
    }
)
async def generate_dragon(request: DragonRequest):
    """
    Generates a dragon-like voice from the input text.
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty or whitespace only.")

    try:
        logger.info(f"Received request: text='{request.text[:50]}...', lang={request.language}")
        
        # Determine Temperature (Instability) based on style
        temperature = 0.75 # Default for neutral
        if request.style == "angry":
            temperature = 0.85 + (0.1 * (request.intensity - 1.0)) # Starts at 0.85, goes up to 0.95 with intensity
            temperature = min(max(temperature, 0.1), 1.0) # Clamp
        elif request.style == "dignified":
            temperature = 0.65 # More stable

        # 1. Generate Raw Audio via XTTS v2
        # Note: This is a blocking operation if running on CPU/GPU without async wrapper, 
        # but since we only have one worker usually for heavy model inference, it's acceptable.
        # For high throughput, we'd offload to a task queue (Celery) or run in a threadpool,
        # but XTTS is heavy so threadpool might not help much if GIL/GPU lock exists.
        # We'll run it directly for now as per simple requirements.
        raw_audio, sample_rate = tts_service.generate_raw_audio(
            request.text, 
            request.language, 
            speed=request.speed,
            temperature=temperature
        )
        
        # 2. Apply Dragon Effects
        wav_bytes = dsp_service.process_audio(
            raw_audio, 
            sample_rate, 
            intensity=request.intensity, 
            style=request.style,
            reverb=request.reverb
        )
        
        logger.info("Audio generation successful.")
        
        # 3. Return Streaming Response (or just bytes for simplicity as it's short audio)
        # Using Response with media_type is effectively sending the bytes.
        return Response(content=wav_bytes, media_type="audio/wav")

    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
