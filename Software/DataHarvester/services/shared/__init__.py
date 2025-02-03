"""
Shared MongoDB and configuration utilities for DataHarvester services.
Provides:
- MongoDB models and repository
- Common database configuration
- Shared schemas
"""

from src.mongodb.models import BaseDocument, CleanedDocument, ProcessedDocument, Document
from src.config.settings import get_settings

__all__ = [
    'BaseDocument',
    'CleanedDocument', 
    'ProcessedDocument',
    'Document',
    'get_settings'
]
