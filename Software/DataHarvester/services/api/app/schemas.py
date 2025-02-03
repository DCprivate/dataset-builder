# Software/DataHarvester/services/data_transformation/interfaces/api/event_schema.py

from datetime import datetime, timezone
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

"""
Event Schema Module

This module defines the Pydantic models that FastAPI uses to validate incoming
HTTP requests. It specifies the expected structure and validation rules for
events entering the system through the API endpoints.
"""


class EventSchema(BaseModel):
    """Schema for event data."""
    id: Optional[str] = None
    data: Dict[str, Any] = Field(default_factory=dict)
    task_context: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        json_schema_extra = {
            "example": {
                "data": {"video_id": "abc123", "channel_id": "xyz789"},
                "task_context": {}
            }
        }
