# Software/DataHarvester/services/data_transformation/src/infrastructure/mongodb/repository.py

from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from domain.interfaces.repository import ITransformationRepository
from domain.models import CleanedDocument, ProcessedDocument

class DataTransformationRepository(ITransformationRepository):
    def __init__(self, mongo_uri: str, database: str, project_name: str):
        self.client = AsyncIOMotorClient(mongo_uri)
        self.db = self.client[database]
        self.project_name = project_name
        self.mongo = self.db[project_name]

    async def get_documents_for_cleaning(self, batch_size: int = 10) -> List[dict]:
        """Fetch raw documents that need cleaning"""
        cursor = self.db.raw_documents.find(
            {"status": "pending"}, 
            limit=batch_size
        )
        return await cursor.to_list(length=batch_size)

    async def store_cleaned_document(self, document: CleanedDocument) -> str:
        result = await self.mongo.insert_one(document.dict())
        return str(result.inserted_id)

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

    async def mark_as_cleaned(self, raw_id: str, cleaned_id: str):
        await self.db.raw_documents.update_one(
            {"_id": raw_id},
            {"$set": {"status": "cleaned", "cleaned_id": cleaned_id}}
        )

    async def get_unprocessed_documents(self, batch_size: int) -> List[dict]:
        cursor = self.mongo.find(
            {"status": "cleaned", "processed": {"$ne": True}},
            limit=batch_size
        )
        return await cursor.to_list(length=batch_size)
