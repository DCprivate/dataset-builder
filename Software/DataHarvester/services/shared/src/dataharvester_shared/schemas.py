# Software/DataHarvester/services/shared/schemas.py

from datetime import datetime, timezone
from pydantic import BaseModel, Field

class EventSchema(BaseModel):
    """Schema for events processed by pipelines"""
    id: str
    data: dict
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    task_context: dict = {}
