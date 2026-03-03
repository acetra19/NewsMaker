"""Central settings loaded from environment."""
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
TEMP_DIR = PROJECT_ROOT / "temp"
ASSETS_DIR = TEMP_DIR / "assets"

# Reddit (PRAW)
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "ContentFarmBot/1.0")

# Subreddits to scout (comma-separated in env, or default)
SUBREDDITS = os.getenv(
    "SUBREDDITS",
    "singularity,ArtificialIntelligence,futurology,technews",
).split(",")
MIN_UPVOTES = int(os.getenv("MIN_UPVOTES", "1000"))

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# ElevenLabs
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "")
USE_EDGE_TTS_FALLBACK = os.getenv("USE_EDGE_TTS_FALLBACK", "true").lower() == "true"

# Pexels
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")

# Replicate (AI images)
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN", "")

# YouTube
YOUTUBE_CLIENT_SECRETS_JSON = os.getenv("YOUTUBE_CLIENT_SECRETS_JSON", str(PROJECT_ROOT / "client_secrets.json"))
YOUTUBE_CREDENTIALS_FILE = PROJECT_ROOT / "youtube_credentials.json"


class Settings:
    """Bundle of all settings for dependency injection."""

    def __init__(self) -> None:
        self.project_root = PROJECT_ROOT
        self.output_dir = OUTPUT_DIR
        self.temp_dir = TEMP_DIR
        self.assets_dir = ASSETS_DIR
        self.reddit_client_id = REDDIT_CLIENT_ID
        self.reddit_client_secret = REDDIT_CLIENT_SECRET
        self.reddit_user_agent = REDDIT_USER_AGENT
        self.subreddits = [s.strip() for s in SUBREDDITS]
        self.min_upvotes = MIN_UPVOTES
        self.openai_api_key = OPENAI_API_KEY
        self.openai_model = OPENAI_MODEL
        self.elevenlabs_api_key = ELEVENLABS_API_KEY
        self.elevenlabs_voice_id = ELEVENLABS_VOICE_ID
        self.use_edge_tts_fallback = USE_EDGE_TTS_FALLBACK
        self.pexels_api_key = PEXELS_API_KEY
        self.replicate_api_token = REPLICATE_API_TOKEN
        self.youtube_credentials_file = YOUTUBE_CREDENTIALS_FILE
        self.youtube_client_secrets = Path(YOUTUBE_CLIENT_SECRETS_JSON)

    def ensure_dirs(self) -> None:
        """Create output and temp directories if missing."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.assets_dir.mkdir(parents=True, exist_ok=True)


_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Return singleton Settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
