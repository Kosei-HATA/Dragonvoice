import io
import numpy as np
import scipy.io.wavfile
from pedalboard import Pedalboard, PitchShift, LowpassFilter, Distortion, Reverb, Bitcrush
from app.config import Config

class DragonDSP:
    def __init__(self):
        # We'll create the board dynamically per request to support intensity
        pass

    def process_audio(self, audio_data: list[float], sample_rate: int, intensity: float = 1.0, style: str = "neutral", reverb: float = 1.0) -> bytes:
        """
        Applies DSP effects to the raw audio and returns WAV bytes.
        Intensity scales the PitchShift and Distortion within the chosen style.
        Reverb scales the wet_level of the reverb effect.
        """
        # Convert list to numpy array (float32)
        audio_np = np.array(audio_data, dtype=np.float32)

        # Base parameters (Style-dependent)
        base_pitch = Config.PITCH_SHIFT_SEMITONES # Default -6.0
        base_drive = Config.DISTORTION_DRIVE_DB     # Default 4.0
        room_size = Config.REVERB_ROOM_SIZE         # Default 0.8
        wet_level = Config.REVERB_WET_LEVEL         # Default 0.35
        bit_depth = 0 # 0 means disabled

        if style == "angry":
            # Angry: Higher tension (less deep), more distortion, closer feel
            # + Bitcrush for "shouting" texture (breaking microphone)
            base_pitch = -5.0 # Revert to previous
            base_drive = 10.0 # Revert to previous base
            room_size = 0.3   # Revert to previous
            wet_level = 0.15  # Revert to previous
            
            # Dynamic Bit Depth: 10 (Base) -> 8 (High Intensity)
            # intensity 1.0 -> 10
            # intensity 1.5 -> 8
            # Formula: 14 - 4*intensity ? 
            # 1.0 -> 10
            # 1.5 -> 8
            # Limit to min 8
            calculated_bit_depth = int(14 - 4 * intensity)
            bit_depth = max(8, min(12, calculated_bit_depth))
            
        elif style == "dignified":
            # Dignified: Deeper, cleaner, larger space
            # Revert to previous liked settings
            base_pitch = -7.0
            base_drive = 2.0
            room_size = 0.95
            wet_level = 0.50

        # Apply Intensity Scaling
        # Pitch: Linear scaling
        pitch_shift = base_pitch * intensity
        
        # Distortion: Quadratic scaling for Angry to reach high levels at high intensity
        if style == "angry":
            # 10.0 * (1.0^2) = 10.0 (Base)
            # 10.0 * (1.5^2) = 22.5 (Matches the "Exaggerated" high that user liked)
            drive_db = base_drive * (intensity ** 2)
        else:
            drive_db = base_drive * intensity
            
        # Apply Reverb Scaling
        # Multiply base wet_level by reverb parameter
        # reverb 0.0 -> 0.0 (Dry)
        # reverb 1.0 -> base wet_level
        # reverb 2.0 -> base wet_level * 2.0 (Max 1.0)
        final_wet_level = min(wet_level * reverb, 1.0)
        
        effects_list = [
            PitchShift(semitones=pitch_shift),
            LowpassFilter(cutoff_frequency_hz=Config.LOW_PASS_CUTOFF_HZ),
            Distortion(drive_db=drive_db),
            Reverb(room_size=room_size, wet_level=final_wet_level)
        ]
        
        if bit_depth > 0:
            # Add Bitcrush if enabled (simulates shouting/clipping)
            # bit_depth usually 8-16. lower is more crushed. 
            effects_list.insert(2, Bitcrush(bit_depth=bit_depth)) # Insert before reverb

        board = Pedalboard(effects_list)

        # Apply effects
        # Pedalboard treats 1D array as mono, which XTTS output is.
        effected_audio = board(audio_np, sample_rate)

        # Convert to WAV format in memory
        byte_io = io.BytesIO()
        
        # scipy.io.wavfile.write expects int16, int32, float32, etc.
        # We'll stick to float32 or convert to int16 if compatibility is needed.
        # float32 is fine for standard WAV.
        scipy.io.wavfile.write(byte_io, sample_rate, effected_audio)
        
        return byte_io.getvalue()

dsp_service = DragonDSP()
