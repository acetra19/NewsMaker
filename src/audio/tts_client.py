"""TTS: ElevenLabs with edge-tts fallback."""
from pathlib import Path
from typing import Optional

from config import get_settings


class TTSClient:
    """Generate narrator audio from script text."""

    def __init__(
        self,
        elevenlabs_key: Optional[str] = None,
        voice_id: Optional[str] = None,
        use_fallback: Optional[bool] = None,
    ) -> None:
        cfg = get_settings()
        self.elevenlabs_key = elevenlabs_key or cfg.elevenlabs_api_key
        self.voice_id = voice_id or cfg.elevenlabs_voice_id
        self.use_fallback = use_fallback if use_fallback is not None else cfg.use_edge_tts_fallback

    def generate(self, text: str, output_path: Path) -> Path:
        """Generate audio file from text. Returns path to saved file."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if not output_path.suffix:
            output_path = output_path.with_suffix(".mp3")

        if self.elevenlabs_key and self.voice_id:
            try:
                return self._elevenlabs(text, output_path)
            except Exception:
                if self.use_fallback:
                    return self._edge_tts(text, output_path)
                raise

        if self.use_fallback:
            return self._edge_tts(text, output_path)
        raise RuntimeError("No TTS configured: set ELEVENLABS or use edge-tts fallback.")

    def _elevenlabs(self, text: str, output_path: Path) -> Path:
        from elevenlabs.client import ElevenLabs

        client = ElevenLabs(api_key=self.elevenlabs_key)
        audio = client.generate(text=text, voice_id=self.voice_id)
        with open(output_path, "wb") as f:
            for chunk in audio:
                if chunk:
                    f.write(chunk)
        return output_path

    def _edge_tts(self, text: str, output_path: Path) -> Path:
        import edge_tts

        # Use mp3 and a default voice
        communicate = edge_tts.Communicate(text, "en-US-GuyNeural")
        communicate.save(str(output_path))
        return output_path
