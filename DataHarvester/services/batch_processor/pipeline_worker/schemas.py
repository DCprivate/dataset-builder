# Software/DataHarvester/services/batch_processor/pipeline_worker/schemas.py

from pydantic import BaseModel

class EventSchema(BaseModel):
    event_type: str
    payload: dict
    metadata: dict = {} 