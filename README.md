# NewsMaker

Automated pipeline: fetch trending Reddit posts from tech/AI subreddits → generate a short video script with GPT → create narrator audio (ElevenLabs or edge-tts) → fetch or generate visuals (Pexels, DALL·E) → assemble a Shorts-style video → optionally upload to YouTube.

Read-only on Reddit; no posting, voting, or moderation.

## Requirements

- **Python 3.10+**
- **ffmpeg** (for video encoding)
- API keys: Reddit (PRAW), OpenAI; optional: ElevenLabs, Pexels, Replicate; YouTube OAuth for upload

## Setup

1. **Clone and enter the repo**
   ```bash
   git clone https://github.com/acetra19/NewsMaker.git
   cd NewsMaker
   ```

2. **Create a virtual environment and install dependencies**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate   # Linux/macOS
   pip install -r requirements.txt
   ```

3. **Configure environment**
   - Copy `.env.example` to `.env`
   - Fill in at least: `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `OPENAI_API_KEY`
   - Optional: `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID`, `PEXELS_API_KEY`, `REPLICATE_API_TOKEN`
   - For YouTube upload: set `YOUTUBE_CLIENT_SECRETS_JSON` and run OAuth once (credentials saved locally)

## Usage

**Generate one video (no upload):**
```bash
python main.py
```
Output is written to the `output/` directory.

**Generate and upload to YouTube:**
```bash
python main.py --upload
```

**Custom output directory:**
```bash
python main.py --output-dir path/to/folder
```

## Docker

```bash
docker build -t newsmaker .
docker run --env-file .env -v $(pwd)/output:/app/output newsmaker
```

## Project structure

| Path | Purpose |
|------|---------|
| `config/` | Settings and env loading |
| `src/scout/` | Reddit API (PRAW): fetch top posts, filter by upvotes |
| `src/scripting/` | GPT script + title/description/hashtags |
| `src/audio/` | TTS (ElevenLabs + edge-tts fallback) |
| `src/visuals/` | Pexels clips + AI images (DALL·E/Replicate) |
| `src/video_engine/` | MoviePy assembly (audio + visuals → MP4) |
| `src/deploy/` | YouTube Data API v3 upload |
| `pipeline.py` | Orchestrates the full flow |
| `main.py` | CLI entry point |

## Docs

- **NewsMaker_masterplan.md** – Strategy, architecture, workflow, and monetization (German/English).

## License

Use and modify as you like. No warranty.
