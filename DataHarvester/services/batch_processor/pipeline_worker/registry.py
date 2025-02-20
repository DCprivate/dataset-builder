# Software/DataHarvester/services/batch_processor/pipeline_worker/registry.py

import logging
from typing import Dict, Type
from .schemas import EventSchema as LocalEventSchema
from .base import Pipeline
from domain.schemas import EventSchema as DomainEventSchema
from domain.infrastructure.mongodb.repository import DataTransformationRepository


"""
Pipeline Registry Module

This module provides a registry system for managing different pipeline types
and their mappings. It determines which pipeline to use based on event attributes,
currently using email addresses as the routing mechanism.
"""


class EventSchema(DomainEventSchema):
    event_type: str
    payload: dict
    metadata: dict = {}


class PipelineRegistry:
    """Registry for managing and routing to different pipeline implementations.

    This class maintains a mapping of pipeline types to their implementations and
    provides logic for determining which pipeline to use based on event attributes.
    It implements a simple factory pattern for pipeline instantiation.

    Attributes:
        pipelines: Dictionary mapping pipeline type strings to pipeline classes
    Example:
        pipelines: Dict[str, Type[Pipeline]] = {
            "support": CustomerSupportPipeline,
            "helpdesk": InternalHelpdeskPipeline,
        }
    """

    pipelines: Dict[str, Type[Pipeline]] = {
        # "support": CustomerSupportPipeline, # Register your pipeline here
    }

    def __init__(self):
        self.repo = DataTransformationRepository(
            mongo_uri="mongodb://localhost:27017",
            database="dataharvester",
            project_name="pipeline_worker"
        )

    @staticmethod
    def get_pipeline_type(event: EventSchema) -> str:
        """
        Implement your logic to determine the pipeline type based on the event.
        
        Example:
            if event.to_email.split("@")[0] == "support":
                return "support"
        """
        raise NotImplementedError(
            "Pipeline routing logic not implemented. Please implement get_pipeline_type() "
            "to determine the appropriate pipeline based on event attributes. "
        ) 

    @staticmethod
    def get_pipeline(event: EventSchema) -> Pipeline:
        """Creates and returns the appropriate pipeline instance for the event.

        Args:
            event: Event schema containing routing information

        Returns:
            Instantiated pipeline object for processing the event
        """
        pipeline_type = PipelineRegistry.get_pipeline_type(event)
        pipeline = PipelineRegistry.pipelines.get(pipeline_type)
        if pipeline:
            logging.info(f"Using pipeline: {pipeline.__name__}")
            return pipeline()
        raise ValueError(f"Unknown pipeline type: {pipeline_type}")
