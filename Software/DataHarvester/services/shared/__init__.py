"""
Shared MongoDB and configuration utilities for DataHarvester services.
Provides:
- MongoDB models and repository
- Common database configuration
- Shared schemas
"""

from dataharvester_shared.mongodb.models import BaseDocument, CleanedDocument, ProcessedDocument, Document
from dataharvester_shared.config.settings import get_settings

__all__ = [
    'BaseDocument',
    'CleanedDocument', 
    'ProcessedDocument',
    'Document',
    'get_settings'
]
