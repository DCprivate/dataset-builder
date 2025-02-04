# Software/DataHarvester/services/api/app/endpoints.py

from abc import ABC, abstractmethod
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from .dependencies import get_db
from .schemas import EventSchema

# Fix these imports to use dataharvester_shared
from dataharvester_shared.schemas import TaskContext
from dataharvester_shared.interfaces import Node

"""
Router Module

This module implements the routing logic for pipeline nodes.
It provides base classes for implementing routing decisions between nodes
in a processing pipeline.
"""

router = APIRouter()

# Define your endpoints here
# Example:
# @router.get("/example")
# async def example_endpoint():
#     return {"message": "This is an example"}

# Export the router
__all__ = ["router"]

class BaseRouter(Node, ABC):
    """Base router class for implementing node routing logic.

    The BaseRouter class provides core routing functionality for directing
    task flow between pipeline nodes. It processes routing rules in sequence
    and falls back to a default node if no rules match.

    Attributes:
        routes: List of RouterNode instances defining routing rules
        fallback: Optional default node to route to if no rules match
    """

    def __init__(self):
        self.routes: List[Node] = []

    def process(self, task_context: TaskContext) -> TaskContext:
        """Processes the routing logic and updates task context.

        Args:
            task_context: Current task execution context

        Returns:
            Updated TaskContext with routing decision recorded
        """
        next_node = self.route(task_context)
        task_context.nodes[self.node_name] = {"next_node": next_node.node_name if next_node else None}
        return task_context

    @abstractmethod
    def route(self, task_context: TaskContext) -> Optional[Node]:
        """Determines the next node based on routing rules.

        Evaluates each routing rule in sequence and returns the first
        matching node. Falls back to the default node if no rules match.

        Args:
            task_context: Current task execution context

        Returns:
            The next node to execute, or None if no route is found
        """
        for route_node in self.routes:
            if route_node.process(task_context):
                return route_node
        return None


class RouterNode(ABC):
    @abstractmethod
    def determine_next_node(self, task_context: TaskContext) -> Optional[Node]:
        pass

    @property
    def node_name(self):
        return self.__class__.__name__

@router.post("/events/", response_model=EventSchema)
async def create_event(event: EventSchema, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Create a new event for processing."""
    try:
        result = await db.events.insert_one(event.model_dump())
        event.id = str(result.inserted_id)
        return event
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/events/{event_id}", response_model=EventSchema)
async def get_event(event_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Get event by ID."""
    event = await db.events.find_one({"_id": event_id})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventSchema(**event)

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
