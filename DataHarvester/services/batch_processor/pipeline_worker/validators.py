# Software/DataHarvester/services/batch_processor/pipeline_worker/validators.py

from domain.interfaces.schema import PipelineSchema

class PipelineValidator:
    def __init__(self, schema: PipelineSchema):
        self.schema = schema
        
    def validate(self):
        # Implementation here
        pass 