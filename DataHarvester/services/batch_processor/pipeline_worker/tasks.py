# Software/DataHarvester/services/worker/pipeline_worker/tasks.py

from .celery_config import celery_app, settings
from domain.interfaces.schema import EventSchema
from domain.infrastructure.mongodb.repository import DataTransformationRepository
from .registry import PipelineRegistry
from datetime import datetime, timezone

"""
Pipeline Task Processing Module

This module handles asynchronous processing of pipeline events using Celery.
It manages the lifecycle of event processing from database retrieval through
pipeline execution and result storage.
"""


@celery_app.task(name="process_incoming_event")
async def process_incoming_event(event_id: str):
    """Processes an incoming event through its designated pipeline.

    This Celery task handles the asynchronous processing of events by:
    1. Retrieving the event from the database
    2. Determining the appropriate pipeline
    3. Executing the pipeline
    4. Storing the results

    Args:
        event_id: Unique identifier of the event to process
    """
    # Initialize repository with settings
    repository = DataTransformationRepository(
        mongo_uri=settings.mongo_uri,
        database=settings.database_name,
        project_name=settings.app_name
    )

    # Retrieve event from database
    db_event = await repository.get_document(event_id)
    if db_event is None:
        raise ValueError(f"Event with id {event_id} not found")

    # Convert to EventSchema
    event = EventSchema(
        id=event_id,
        data=db_event.get('data', {}),
        created_at=db_event.get('created_at') or datetime.now(timezone.utc),
        task_context=db_event.get('task_context', {})
    )

    # Process through pipeline
    pipeline = PipelineRegistry.get_pipeline(event)
    task_context = pipeline.run(event).model_dump(mode="json")
    
    # Update event with results
    await repository.update_document(event_id, {"task_context": task_context})
