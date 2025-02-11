# Software/DataHarvester/services/data_transformation/domain/services/event.py

from datetime import datetime
import uuid
from beanie import Document
from pydantic import Field

"""
Event Database Model Module

This module defines the Beanie ODM model for storing events in MongoDB.
It provides two main storage components:
1. Raw event data (data field): Stores the original incoming event
2. Processing results (task_context field): Stores the pipeline processing results

This model leverages Beanie's Document class which provides MongoDB ODM functionality
and automatic schema validation through Pydantic.
"""


class Event(Document):
    """Beanie ODM model for storing events and their processing results.

    This model serves as the primary storage for both incoming events and
    their processing results. It uses MongoDB's native document structure
    for flexible schema storage of both raw data and processing context.

    Attributes:
        id: UUID primary key, auto-generated
        data: Raw event data as received by the API
        task_context: Results and metadata from pipeline processing
        created_at: Timestamp of event creation
        updated_at: Timestamp of last update
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid1()))
    data: dict = Field(description="Raw event data as received from the API")
    task_context: dict = Field(description="Processing results and metadata")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "events"
