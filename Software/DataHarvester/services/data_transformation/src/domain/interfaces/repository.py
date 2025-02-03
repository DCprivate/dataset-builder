# Software/DataHarvester/services/data_transformation/domain/interfaces/repository.py

from abc import ABC, abstractmethod
from typing import List, Dict

class ITransformationRepository(ABC):
    @abstractmethod
    async def get_documents_for_cleaning(self, batch_size: int) -> List[Dict]:
        """Get documents that need cleaning"""
        pass

    @abstractmethod
    async def store_cleaned_document(self, raw_id: str, cleaned_content: str) -> str:
        """Store cleaned document"""
        pass

    @abstractmethod
    async def get_documents_for_processing(self, batch_size: int) -> List[Dict]:
        """Get documents that need processing"""
        pass

    @abstractmethod
    async def store_processed_document(self, cleaned_id: str, processed_content: str, analysis_results: dict) -> str:
        """Store processed document"""
        pass