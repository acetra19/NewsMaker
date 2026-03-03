"""Generate 45–60s video scripts from Reddit posts using GPT."""
from dataclasses import dataclass
from typing import List, Optional

from openai import OpenAI

from config import get_settings
from src.scout import RedditPost


@dataclass
class VideoScript:
    """Generated script and metadata for one video."""

    text: str
    sentences: List[str]
    title: str
    description: str
    hashtags: List[str]
    source_post_id: str


SCRIPT_SYSTEM = """You are a Viral Short Video Creator for YouTube Shorts and TikTok.
Your scripts are 45–60 seconds when read aloud (about 120–150 words).
Structure every script as:
1. HOOK (0–3 sec): One punchy line that grabs attention.
2. STORY/INFO: Facts and a bit of "fear of missing out."
3. CONCLUSION/CTA: End with a question or call to the viewer.
Use simple, spoken English. Short sentences. No bullet points in the script body."""


class ScriptGenerator:
    """Turn Reddit posts into video scripts via OpenAI."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        cfg = get_settings()
        self.client = OpenAI(api_key=api_key or cfg.openai_api_key)
        self.model = model or cfg.openai_model

    def _build_prompt(self, post: RedditPost) -> str:
        comments_block = "\n".join(f"- {c}" for c in post.top_comments[:3])
        return f"""Create a short viral video script from this Reddit post.

Title: {post.title}

Post body:
{post.selftext or "(no body)"}

Top comments (for context/controversy):
{comments_block}

Respond with ONLY the script text, one paragraph or short lines. No labels like "Hook:" or "CTA:" in the output."""

    def generate(self, post: RedditPost) -> VideoScript:
        """Generate script and metadata for one Reddit post."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SCRIPT_SYSTEM},
                {"role": "user", "content": self._build_prompt(post)},
            ],
            max_tokens=500,
        )
        text = (response.choices[0].message.content or "").strip()
        sentences = [s.strip() for s in text.replace("\n", " ").split(". ") if s.strip()]
        if not sentences:
            sentences = [text]

        meta_response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"Based on this short video script, give:\n1. A catchy YouTube Shorts title (under 60 chars)\n2. A 1–2 sentence description\n3. 5 hashtags (no # in output, comma-separated)\n\nScript:\n{text}",
                },
            ],
            max_tokens=200,
        )
        meta = (meta_response.choices[0].message.content or "").strip()
        lines = [l.strip() for l in meta.split("\n") if l.strip()]
        title = lines[0][:60] if lines else post.title[:60]
        description = lines[1] if len(lines) > 1 else ""
        hashtags = []
        if len(lines) > 2:
            hashtags = [t.strip() for t in lines[2].replace("#", "").split(",")][:5]

        return VideoScript(
            text=text,
            sentences=sentences,
            title=title,
            description=description,
            hashtags=hashtags,
            source_post_id=post.post_id,
        )
