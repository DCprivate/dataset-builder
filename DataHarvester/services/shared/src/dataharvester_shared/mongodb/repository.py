# Software/DataHarvester/services/shared/mongodb/repository.py

from typing import List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from .models import CleanedDocument, ProcessedDocument

class MongoRepository:
    """Base MongoDB repository implementation"""
    
    def __init__(self, mongo_uri: str, database: str, project_name: str):
        self.client = AsyncIOMotorClient(mongo_uri)
        self.db = self.client[database]
        self.project = project_name
        
    async def get_uncleaned_documents(self, batch_size: int) -> List[Dict[str, Any]]:
        """Get documents that need cleaning"""
        cursor = self.db.raw_documents.find(
            {"status": "raw", "project": self.project}
        ).limit(batch_size)
        return await cursor.to_list(length=batch_size)

    async def store_cleaned_document(self, document: CleanedDocument) -> str:
        """Store cleaned document"""
        result = await self.db.cleaned_documents.insert_one(document.model_dump())
        return str(result.inserted_id)

    async def mark_as_cleaned(self, raw_id: str, cleaned_id: str) -> None:
        """Update raw document status"""
        await self.db.raw_documents.update_one(
            {"_id": raw_id},
            {"$set": {"status": "cleaned", "cleaned_id": cleaned_id}}
        )

    async def get_unprocessed_documents(self, batch_size: int) -> List[Dict[str, Any]]:
        """Get documents that need processing"""
        cursor = self.db.cleaned_documents.find(
            {"status": "cleaned", "project": self.project}
        ).limit(batch_size)
        return await cursor.to_list(length=batch_size)

    async def store_processed_document(self, document: ProcessedDocument) -> str:
        """Store processed document"""
        result = await self.db.processed_documents.insert_one(document.model_dump())
        return str(result.inserted_id)

    async def mark_as_processed(self, cleaned_id: str, processed_id: str) -> None:
        """Update cleaned document status"""
        await self.db.cleaned_documents.update_one(
            {"_id": cleaned_id},
            {"$set": {"status": "processed", "processed_id": processed_id}}
        )

    async def get_document(self, doc_id: str) -> Dict[str, Any]:
        """Get document by ID"""
        result = await self.db.documents.find_one({"_id": doc_id})
        if result is None:
            raise ValueError(f"Document {doc_id} not found")
        return dict(result)

    async def update_document(self, doc_id: str, update_data: Dict[str, Any]) -> None:
        """Update document by ID"""
        await self.db.documents.update_one(
            {"_id": doc_id},
            {"$set": update_data}
        ) 