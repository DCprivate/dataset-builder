# Software/DataHarvester/services/scraper_service/domain/models/transcript.py

from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel

class TranscriptSegment(BaseModel):
    """Model for individual transcript entries."""
    text: str
    start: float
    duration: float

class RawTranscript(BaseModel):
    """Model for raw transcript data from YouTube."""
    video_id: str
    segments: List[TranscriptSegment]
    language: str
    created_at: datetime
    metadata: Dict[str, Any] = {}
    channel_id: Optional[str] = None
    updated_at: Optional[datetime] = None

class ProcessedTranscript(BaseModel):
    """Model for cleaned and processed transcript data."""
    video_id: str
    channel_id: Optional[str]
    full_text: str
    metadata: Dict[str, Any]
    word_count: int
    language: str
    processing_stats: Dict[str, Any]
    created_at: datetime = datetime.now()
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