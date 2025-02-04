# Software/DataHarvester/services/shared/src/dataharvester_shared/schemas.py

from datetime import datetime, timezone
from typing import List, Type, Optional, Dict
from pydantic import BaseModel, Field
from dataharvester_shared.interfaces.base import Node

class EventSchema(BaseModel):
    """Schema for events processed by pipelines"""
    id: str
    data: dict
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    task_context: Dict = Field(default_factory=dict)

class NodeConfig(BaseModel):
    """Configuration model for pipeline nodes."""
    node: Type[Node]
    connections: List[Type[Node]] = Field(default_factory=list)
    is_router: bool = False
    description: Optional[str] = None

class PipelineSchema(BaseModel):
    """Schema definition for a complete pipeline."""
    description: Optional[str] = None
    start: Type[Node]
    nodes: List[NodeConfig]
