# Software/DataHarvester/src/infrastructure/database/models.py

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from dataclasses import dataclass

@dataclass
class TranscriptSegment:
    """Model for individual transcript entries."""
    text: List[str]
    start: float
    duration: float

@dataclass
class RawTranscript:
    """Model for raw transcript data from YouTube."""
    video_id: str
    channel_id: Optional[str]
    segments: List[TranscriptSegment]
    metadata: Dict[str, Any]  # title, description, etc.
    processed: bool = False
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            'video_id': self.video_id,
            'channel_id': self.channel_id,
            'segments': [vars(segment) for segment in self.segments],
            'metadata': self.metadata,
            'processed': self.processed,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

@dataclass
class ProcessedTranscript:
    """Model for cleaned and processed transcript data."""
    video_id: str
    channel_id: Optional[str]
    full_text: str
    metadata: Dict[str, Any]
    word_count: int
    language: str
    processing_stats: Dict[str, Any]  # cleaning stats, token counts, etc.
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            'video_id': self.video_id,
            'channel_id': self.channel_id,
            'full_text': self.full_text,
            'metadata': self.metadata,
            'word_count': self.word_count,
            'language': self.language,
            'processing_stats': self.processing_stats,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }