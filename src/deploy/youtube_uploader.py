"""Upload rendered video to YouTube via Data API v3."""
from pathlib import Path
from typing import List, Optional

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from config import get_settings


SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


class YouTubeUploader:
    """Upload video and set title, description, tags (Shorts)."""

    def __init__(self, credentials_path: Optional[Path] = None) -> None:
        cfg = get_settings()
        self.credentials_path = credentials_path or cfg.youtube_credentials_file
        self._youtube = None

    def _get_credentials(self):
        creds = None
        if self.credentials_path.exists():
            creds = Credentials.from_authorized_user_file(str(self.credentials_path), SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # User must run OAuth flow; need client_secrets JSON path
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(get_settings().youtube_client_secrets), SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open(self.credentials_path, "w") as f:
                f.write(creds.to_json())
        return creds

    def _get_client(self):
        if self._youtube is None:
            creds = self._get_credentials()
            self._youtube = build("youtube", "v3", credentials=creds)
        return self._youtube

    def upload(
        self,
        video_path: Path,
        title: str,
        description: str = "",
        tags: Optional[List[str]] = None,
        category_id: str = "28",
    ) -> Optional[str]:
        """Upload video; return video ID or None on failure."""
        video_path = Path(video_path)
        if not video_path.exists():
            return None
        body = {
            "snippet": {
                "title": title[:100],
                "description": description[:5000],
                "tags": tags or [],
                "categoryId": category_id,
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
            },
        }
        media = MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True)
        try:
            request = self._get_client().videos().insert(
                part="snippet,status",
                body=body,
                media_body=media,
            )
            response = request.execute()
            return response.get("id")
        except Exception:
            return None
