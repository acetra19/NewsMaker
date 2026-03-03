"""Orchestrate full flow: Reddit -> script -> audio -> visuals -> video -> optional upload."""
from pathlib import Path
from typing import Optional

from config import get_settings
from src.scout import RedditScout, RedditPost
from src.scripting import ScriptGenerator, VideoScript
from src.audio import TTSClient
from src.visuals import ImageGenerator, VisualAsset
from src.video_engine import VideoAssembler
from src.deploy import YouTubeUploader


def run_pipeline(
    upload_to_youtube: bool = False,
    output_dir: Optional[Path] = None,
) -> Optional[Path]:
    """Run one full cycle: fetch candidate, generate script, assets, video; optionally upload."""
    settings = get_settings()
    settings.ensure_dirs()
    out = output_dir or settings.output_dir
    temp = settings.temp_dir
    assets = settings.assets_dir

    # 1. Scout
    scout = RedditScout()
    candidates = scout.fetch_candidates(time_filter="day", limit=10)
    if not candidates:
        return None
    post = candidates[0]

    # 2. Script
    script_gen = ScriptGenerator()
    script = script_gen.generate(post)

    # 3. Audio
    audio_path = temp / f"audio_{post.post_id}.mp3"
    tts = TTSClient()
    tts.generate(script.text, audio_path)

    # 4. Visuals
    img_gen = ImageGenerator()
    visual_assets = img_gen.get_assets_for_sentences(script.sentences, segment_duration_sec=4.0)
    if not visual_assets:
        # Placeholder: one black frame per sentence would go here; for now use single duration
        pass

    # 5. Assemble
    video_path = out / f"short_{post.post_id}.mp4"
    assembler = VideoAssembler()
    assembler.assemble(audio_path, visual_assets, video_path)

    # 6. Optional upload
    if upload_to_youtube:
        uploader = YouTubeUploader()
        uploader.upload(
            video_path,
            title=script.title,
            description=script.description,
            tags=script.hashtags,
        )

    return video_path
