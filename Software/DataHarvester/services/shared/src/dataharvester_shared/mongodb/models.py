# Software/DataHarvester/services/shared/mongodb/models.py

from datetime import datetime, timezone
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class BaseDocument(BaseModel):
    """Base document model with common fields"""
    id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)

class CleanedDocument(BaseDocument):
    """Model for cleaned documents"""
    raw_id: str
    content: str
    status: str = "cleaned"

class ProcessedDocument(BaseDocument):
    """Model for processed documents"""
    cleaned_id: str
    content: str
    analysis_results: Dict[str, Any]
    status: str = "processed"

class Document(BaseDocument):
    """Model for general documents"""
    data: Dict[str, Any]
    task_context: Dict[str, Any] = Field(default_factory=dict)
    status: str = "pending" 