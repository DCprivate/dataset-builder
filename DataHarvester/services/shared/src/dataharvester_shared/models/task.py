# /Software/DataHarvester/services/shared/src/dataharvester_shared/models/task.py

from typing import Dict, Any
from pydantic import BaseModel, Field
from ..schemas import EventSchema

class TaskContext(BaseModel):
    """Task execution context."""
    event: EventSchema
    nodes: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict) 