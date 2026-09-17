from fastapi import FastAPI

from controllers.tts_controller import router as tts_router


app = FastAPI(
    title="Neutonsoft AI TTS Worker",
    version="1.0.0"
)


app.include_router(tts_router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "tts-worker"
    }