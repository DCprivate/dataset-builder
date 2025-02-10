# Software/DataHarvester/services/data_transformation/src/infrastructure/mongodb/factory.py

from typing import Optional
from .repository import DataTransformationRepository

class MongoRepositoryFactory:
    _instance: Optional[DataTransformationRepository] = None

    @classmethod
    def create(cls, mongo_uri: str, database: str, project_name: str) -> DataTransformationRepository:
        """Create or return existing repository instance"""
        if not cls._instance:
            cls._instance = DataTransformationRepository(mongo_uri, database, project_name)
        return cls._instance