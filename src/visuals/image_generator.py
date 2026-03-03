"""AI image generation (Replicate/Flux) and asset list for video."""
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from openai import OpenAI

from config import get_settings
from src.visuals.pexels_client import PexelsClient


@dataclass
class VisualAsset:
    """Single visual for a segment: path and duration hint in seconds."""

    path: Path
    duration_sec: float
    is_video: bool


class ImageGenerator:
    """Get images for script segments: Pexels first, then AI-generated."""

    def __init__(
        self,
        pexels_key: Optional[str] = None,
        replicate_token: Optional[str] = None,
    ) -> None:
        cfg = get_settings()
        self.pexels = PexelsClient(api_key=pexels_key or cfg.pexels_api_key)
        self.replicate_token = replicate_token or cfg.replicate_api_token
        self.openai_client = OpenAI(api_key=cfg.openai_api_key) if cfg.openai_api_key else None
        self.assets_dir = cfg.assets_dir

    def get_assets_for_sentences(
        self,
        sentences: List[str],
        segment_duration_sec: float = 4.0,
    ) -> List[VisualAsset]:
        """Return list of VisualAsset (path, duration) for each sentence/segment."""
        assets: List[VisualAsset] = []
        for i, sentence in enumerate(sentences):
            path = self._get_image_or_clip(sentence, index=i)
            if path:
                assets.append(
                    VisualAsset(path=path, duration_sec=segment_duration_sec, is_video=path.suffix.lower() in (".mp4", ".mov"))
                )
        return assets

    def _get_image_or_clip(self, prompt: str, index: int = 0) -> Optional[Path]:
        """Try Pexels search, then AI image. Save to assets_dir and return path."""
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        # Simple keyword extraction: first few words
        query = " ".join(prompt.split()[:5])
        videos = self.pexels.search_videos(query, per_page=1) if self.pexels.api_key else []
        if videos:
            url = self.pexels.get_best_video_file(videos[0])
            if url:
                path = self.assets_dir / f"seg_{index}.mp4"
                self.pexels.download_clip(url, path)
                return path
        # Fallback: DALL-E if OpenAI key present
        if self.openai_client:
            path = self.assets_dir / f"seg_{index}.png"
            try:
                resp = self.openai_client.images.generate(
                    model="dall-e-3",
                    prompt=prompt[:1000],
                    size="1024x1024",
                    n=1,
                )
                img_url = resp.data[0].url
                if img_url:
                    import httpx
                    r = httpx.get(img_url)
                    r.raise_for_status()
                    path.write_bytes(r.content)
                    return path
            except Exception:
                pass
        return None
