from pydantic import BaseModel

class CleanedDocument(BaseModel):
    raw_id: str
    content: str

class ProcessedDocument(BaseModel):
    cleaned_id: str
    content: str
    analysis_results: dict

class TaskContext(BaseModel):
    raw_data: dict
    processing_steps: list = []
    results: dict = {}
    errors: list = []

class EventSchema(BaseModel):
    event_type: str
    payload: dict
    metadata: dict = {}

class PipelineSchema(BaseModel):
    pipeline_type: str
    config: dict
    version: str = "1.0"