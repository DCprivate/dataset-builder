from __future__ import annotations

from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi

from dataset_builder.ingest.base import BaseIngester
from dataset_builder.models import NormalizedDocument
from dataset_builder.utils import normalize_whitespace, sha256_text


class YouTubeIngester(BaseIngester):
    @staticmethod
    def _extract_video_id(value: str) -> str:
        parsed = urlparse(value)
        if parsed.hostname in {"youtu.be"}:
            return parsed.path.lstrip("/")
        if parsed.hostname and "youtube.com" in parsed.hostname:
            query = parse_qs(parsed.query)
            if "v" in query:
                return query["v"][0]
        if len(value) == 11 and "/" not in value:
            return value
        raise ValueError(f"Could not parse YouTube video id from: {value}")

    def ingest(self, value: str) -> NormalizedDocument:
        video_id = self._extract_video_id(value)
        fetched = YouTubeTranscriptApi().fetch(video_id)

        parts: list[str] = []
        transcript_meta: list[dict] = []
        for item in fetched:
            text = (item.text or "").strip()
            if text:
                parts.append(text)
                transcript_meta.append(
                    {
                        "text": text,
                        "start": float(item.start),
                        "duration": float(item.duration),
                    }
                )

        joined = normalize_whitespace(" ".join(parts))
        doc_id = sha256_text(f"youtube::{video_id}::{joined[:4000]}")

        return NormalizedDocument(
            doc_id=doc_id,
            source_type="youtube",
            source_uri=value,
            title=f"youtube-{video_id}",
            text=joined,
            metadata={"video_id": video_id, "segments": transcript_meta},
        )
