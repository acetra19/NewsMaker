"""Compose final video from audio and visual assets using MoviePy."""
from pathlib import Path
from typing import List, Optional

from moviepy.editor import (
    AudioFileClip,
    ImageClip,
    TextClip,
    concatenate_videoclips,
    CompositeVideoClip,
    VideoFileClip,
)

from config import get_settings
from src.visuals import VisualAsset


class VideoAssembler:
    """Build one video from audio track and list of visual assets."""

    def __init__(self) -> None:
        self.settings = get_settings()

    def assemble(
        self,
        audio_path: Path,
        assets: List[VisualAsset],
        output_path: Path,
        fps: int = 24,
    ) -> Path:
        """Create final video: audio + visuals cut every 3–5 sec, optional Ken Burns on images."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if not output_path.suffix:
            output_path = output_path.with_suffix(".mp4")

        audio = AudioFileClip(str(audio_path))
        duration = audio.duration
        clips = []
        used_duration = 0.0

        for asset in assets:
            if used_duration >= duration:
                break
            seg_dur = min(asset.duration_sec, duration - used_duration)
            if asset.is_video:
                clip = VideoFileClip(str(asset.path)).subclip(0, seg_dur)
            else:
                clip = ImageClip(str(asset.path)).with_duration(seg_dur)
                # Optional: resize to 1080x1920 for Shorts
                clip = clip.resize(height=1920) if clip.h > 1920 else clip
            clips.append(clip)
            used_duration += seg_dur

        if not clips:
            # Single black frame with audio if no assets
            from moviepy.editor import ColorClip
            clip = ColorClip(size=(1080, 1920), color=(0, 0, 0)).with_duration(duration)
            clip = clip.with_audio(audio)
            clip.write_videofile(str(output_path), fps=fps, codec="libx264", audio_codec="aac")
            clip.close()
            audio.close()
            return output_path

        video = concatenate_videoclips(clips)
        video = video.with_audio(audio)
        video.write_videofile(str(output_path), fps=fps, codec="libx264", audio_codec="aac")

        for c in clips:
            c.close()
        video.close()
        audio.close()
        return output_path
