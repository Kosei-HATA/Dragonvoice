from pydantic import BaseModel, Field

class DragonRequest(BaseModel):
    text: str = Field(..., description="The text to be spoken by the dragon.")
    language: str = Field(default="en", description="Language code (e.g., 'en', 'ja').")
    speed: float = Field(default=1.0, ge=0.5, le=2.0, description="Speech speed (0.5 to 2.0). Higher is faster.")
    intensity: float = Field(default=1.0, ge=0.0, le=2.0, description="Dragon intensity/vigor (0.0 to 2.0). Higher is deeper and more distorted.")
    style: str = Field(default="neutral", pattern="^(neutral|angry|dignified)$", description="Voice style: 'neutral', 'angry', or 'dignified'.")
    reverb: float = Field(default=1.0, ge=0.0, le=2.0, description="Reverb amount (0.0 to 2.0). 1.0 is style default.")
    class Config:
        json_schema_extra = {
            "example": {
                "text": "吾輩はドラゴンである。",
                "language": "ja"
            }
        }
