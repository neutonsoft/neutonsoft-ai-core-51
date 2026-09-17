from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from schemas.tts_schema import TTSRequest
from services.tts_service import generate_speech, OUTPUT_DIR

router = APIRouter(prefix="/tts", tags=["TTS"])


@router.post("/generate")
def generate_tts(request: TTSRequest):
    print("=====================================")
    print("TTS REQUEST RECEIVED")
    print("=====================================")
    print("Text:", request.text)
    print("Language:", request.language)
    print("Voice ID:", request.voiceId)
    print("=====================================")

    result = generate_speech(request.text, request.voiceId, request.speed)

    return {
        "success": True,
        "message": "TTS generated successfully",
        "data": {**result, "text": request.text, "language": request.language},
    }


@router.get("/audio/{file_name}")
def get_audio(file_name: str):
    file_path = OUTPUT_DIR / file_name

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")

    return FileResponse(path=str(file_path), media_type="audio/wav", filename=file_name)
