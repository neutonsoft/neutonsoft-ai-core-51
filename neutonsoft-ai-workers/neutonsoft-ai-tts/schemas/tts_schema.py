from pydantic import BaseModel, Field

class TTSRequest(BaseModel):
    text: str
    language: str = "en-US"
    voiceId: str | None = None
    speed: float = Field(default=1.0, ge=0.5, le=2.0)