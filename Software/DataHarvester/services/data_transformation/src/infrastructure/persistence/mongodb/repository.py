# Software/DataHarvester/services/data_transformation/infrastructure/persistence/mongodb/repository.py

from typing import List, Optional
from datetime import datetime
from shared.mongodb.repository import MongoRepository
from shared.mongodb.models import CleanedDocument, ProcessedDocument
from domain.interfaces.repository import ITransformationRepository

class DataTransformationRepository(ITransformationRepository):
    def __init__(self, mongo_uri: str, database: str, project_name: str):
        self.mongo = MongoRepository(mongo_uri, database, project_name)

    async def get_documents_for_cleaning(self, batch_size: int = 10) -> List[dict]:
        """Fetch raw documents that need cleaning"""
        return await self.mongo.get_uncleaned_documents(batch_size)

    async def store_cleaned_document(self, raw_id: str, cleaned_content: str) -> str:
        """Store cleaned document and update raw document status"""
        document = CleanedDocument(
            raw_id=raw_id,
            content=cleaned_content
        )
        cleaned_id = await self.mongo.store_cleaned_document(document)
        await self.mongo.mark_as_cleaned(raw_id, cleaned_id)
        return cleaned_id

    async def get_documents_for_processing(self, batch_size: int = 10) -> List[dict]:
        """Fetch cleaned documents that need processing"""
        return await self.mongo.get_unprocessed_documents(batch_size)

    async def store_processed_document(self, cleaned_id: str, processed_content: str, analysis_results: dict) -> str:
        """Store processed document and update cleaned document status"""
        document = ProcessedDocument(
            cleaned_id=cleaned_id,
            content=processed_content,
            analysis_results=analysis_results
        )
        processed_id = await self.mongo.store_processed_document(document)
        await self.mongo.mark_as_processed(cleaned_id, processed_id)
        return processed_id
