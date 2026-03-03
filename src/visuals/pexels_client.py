"""Fetch stock video clips from Pexels API."""
from pathlib import Path
from typing import List, Optional
from urllib.request import urlretrieve

import httpx

from config import get_settings


class PexelsClient:
    """Download Pexels video clips by search query."""

    BASE = "https://api.pexels.com"

    def __init__(self, api_key: Optional[str] = None) -> None:
        cfg = get_settings()
        self.api_key = api_key or cfg.pexels_api_key
        self._client = httpx.Client(
            headers={"Authorization": self.api_key},
            timeout=30.0,
        )

    def search_videos(self, query: str, per_page: int = 5) -> List[dict]:
        """Return list of video dicts from Pexels (id, url, duration, etc.)."""
        if not self.api_key:
            return []
        r = self._client.get(
            f"{self.BASE}/videos/search",
            params={"query": query, "per_page": per_page},
        )
        r.raise_for_status()
        data = r.json()
        return data.get("videos", [])

    def download_clip(self, video_url: str, save_path: Path) -> Path:
        """Download one video file to save_path."""
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        # Pexels returns video files in video_files; use best quality available
        resp = self._client.get(video_url)
        resp.raise_for_status()
        save_path.write_bytes(resp.content)
        return save_path

    def get_best_video_file(self, video: dict) -> Optional[str]:
        """Extract best quality video file URL from Pexels video object."""
        files = video.get("video_files", [])
        if not files:
            return None
        # Prefer HD, then SD
        for quality in ["hd", "sd"]:
            for f in files:
                if f.get("quality") == quality and f.get("width", 0) >= 720:
                    return f.get("link")
        return files[0].get("link") if files else None
