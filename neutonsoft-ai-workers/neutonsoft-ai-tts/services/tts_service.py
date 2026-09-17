from pathlib import Path
from uuid import uuid4
import wave

from piper.voice import PiperVoice
from piper import SynthesisConfig


BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)


# ============================================================
# Available Voices
# ============================================================

VOICE_MODELS = {
    "en_US-lessac-medium": MODELS_DIR / "en_US-lessac-medium.onnx",
    "en_US-ryan-high": MODELS_DIR / "en_US-ryan-high.onnx",
}


# ============================================================
# Load Voices
# ============================================================

print("[TTS SERVICE] Loading Piper voices...")

voices = {}

for voice_id, model_path in VOICE_MODELS.items():
    if not model_path.exists():
        raise FileNotFoundError(
            f"TTS model not found: {model_path}"
        )

    print(f"[TTS SERVICE] Loading voice: {voice_id}")

    voices[voice_id] = PiperVoice.load(
        str(model_path)
    )

print(
    f"[TTS SERVICE] Piper voices loaded: {list(voices.keys())}"
)


# ============================================================
# Generate Speech
# ============================================================

def generate_speech(
    text: str,
    voice_id: str = "en_US-ryan-high",
    speed: float = 1.0,
):
    # --------------------------------------------------------
    # Validate Voice
    # --------------------------------------------------------

    if voice_id not in voices:
        raise ValueError(
            f"Invalid voiceId: {voice_id}"
        )

    voice = voices[voice_id]

    # --------------------------------------------------------
    # Output File
    # --------------------------------------------------------

    file_name = f"{uuid4()}.wav"
    output_path = OUTPUT_DIR / file_name

    # --------------------------------------------------------
    # Speed
    # --------------------------------------------------------
    #
    # Our API:
    # 1.0 = normal
    # 1.2 = faster
    # 0.8 = slower
    #
    # Piper:
    # lower length_scale = faster
    # higher length_scale = slower
    # --------------------------------------------------------

    length_scale = 1.0 / speed

    synthesis_config = SynthesisConfig(
        length_scale=length_scale,
    )

    # --------------------------------------------------------
    # Generate WAV
    # --------------------------------------------------------

    print(
        f"[TTS SERVICE] Generating speech "
        f"voice={voice_id}, speed={speed}"
    )

    with wave.open(str(output_path), "wb") as wav_file:
        voice.synthesize_wav(
            text,
            wav_file,
            syn_config=synthesis_config,
        )

    print(
        f"[TTS SERVICE] Audio generated: {file_name}"
    )

    return {
        "fileName": file_name,
        "filePath": str(output_path),
        "voiceId": voice_id,
        "speed": speed,
    }