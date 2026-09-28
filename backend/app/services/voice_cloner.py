import httpx
import logging
from ..core.config import settings

logger = logging.getLogger(__name__)

class VoiceClonerService:
    """
    Synthesizes speech using cloned voice models.
    Supports ElevenLabs API for fast zero-maintenance synthesis,
    with fallback or self-hosted integration to F5-TTS / CosyVoice.
    """
    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY

    async def create_voice_clone(self, voice_name: str, clean_audio_path: str) -> str:
        """
        Registers reference audio to create a voice clone embedding.
        Returns the unique voice_id.
        """
        if not self.api_key:
            logger.warning("No ElevenLabs API key found. Simulating voice clone creation.")
            return f"simulated_voice_{voice_name.lower()}_123"

        url = "https://api.elevenlabs.io/v1/voices/add"
        headers = {"xi-api-key": self.api_key}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            with open(clean_audio_path, "rb") as f:
                files = {"files": (clean_audio_path, f, "audio/mpeg")}
                data = {"name": voice_name, "description": "Memorial voice clone"}
                response = await client.post(url, headers=headers, data=data, files=files)
                response.raise_for_status()
                result = response.json()
                return result["voice_id"]

    async def synthesize_speech(self, voice_id: str, script_text: str, output_path: str) -> str:
        """
        Synthesizes script text into speech audio file (.mp3/.wav).
        """
        if not self.api_key or voice_id.startswith("simulated_"):
            logger.warning("Synthesizing in mock/local mode.")
            # Mock generating audio file
            with open(output_path, "wb") as f:
                f.write(b"MOCK_AUDIO_DATA")
            return output_path

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "text": script_text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.55,
                "similarity_boost": 0.85
            }
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            with open(output_path, "wb") as f:
                f.write(response.content)
            return output_path
