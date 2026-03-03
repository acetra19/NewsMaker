"""Fetch and filter top Reddit posts for video content."""
from dataclasses import dataclass
from typing import List, Optional

import praw
from praw.models import Submission

from config import get_settings


@dataclass
class RedditPost:
    """Single post suitable for video scripting."""

    title: str
    selftext: str
    subreddit: str
    score: int
    url: str
    top_comments: List[str]
    post_id: str


class RedditScout:
    """Scout subreddits for viral posts meeting minimum upvotes."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        user_agent: Optional[str] = None,
        subreddits: Optional[List[str]] = None,
        min_upvotes: Optional[int] = None,
    ) -> None:
        cfg = get_settings()
        self.client_id = client_id or cfg.reddit_client_id
        self.client_secret = client_secret or cfg.reddit_client_secret
        self.user_agent = user_agent or cfg.reddit_user_agent
        self.subreddit_names = subreddits or cfg.subreddits
        self.min_upvotes = min_upvotes or cfg.min_upvotes
        self._reddit: Optional[praw.Reddit] = None

    def _get_reddit(self) -> praw.Reddit:
        if self._reddit is None:
            self._reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent=self.user_agent,
            )
        return self._reddit

    def _get_top_comments(self, submission: Submission, limit: int = 3) -> List[str]:
        submission.comment_sort = "top"
        submission.comment_limit = limit
        comments = []
        for c in submission.comments:
            if hasattr(c, "body") and not c.body.startswith("["):
                comments.append(c.body[:500])
            if len(comments) >= limit:
                break
        return comments

    def fetch_candidates(self, time_filter: str = "day", limit: int = 25) -> List[RedditPost]:
        """Fetch top posts from configured subreddits, filtered by min_upvotes."""
        reddit = self._get_reddit()
        results: List[RedditPost] = []
        seen_ids = set()

        for sub_name in self.subreddit_names:
            try:
                sub = reddit.subreddit(sub_name)
                for submission in sub.top(time_filter=time_filter, limit=limit):
                    if submission.id in seen_ids:
                        continue
                    if submission.score < self.min_upvotes:
                        continue
                    # Skip link-only posts without meaningful text
                    text = (submission.selftext or "").strip()
                    if not text and not submission.title:
                        continue
                    seen_ids.add(submission.id)
                    top_comments = self._get_top_comments(submission)
                    results.append(
                        RedditPost(
                            title=submission.title,
                            selftext=text[:2000],
                            subreddit=sub_name,
                            score=submission.score,
                            url=f"https://reddit.com{submission.permalink}",
                            top_comments=top_comments,
                            post_id=submission.id,
                        )
                    )
            except Exception:
                continue

        return sorted(results, key=lambda p: p.score, reverse=True)
