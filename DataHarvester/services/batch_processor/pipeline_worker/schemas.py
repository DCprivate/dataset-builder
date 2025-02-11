from pydantic import BaseModel

class EventSchema(BaseModel):
    event_type: str
    payload: dict
    metadata: dict = {} 