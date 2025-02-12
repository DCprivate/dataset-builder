# Software/DataHarvester/services/scraper_service/infrastructure/error_handling/error_registry.py

from typing import Dict, Type, Callable
from .exceptions.specific import DatabaseError, ScrapingError, ValidationError
from pymongo import errors as mongo_errors
from youtube_transcript_api import (
    NoTranscriptFound, 
    TranscriptsDisabled, 
    VideoUnavailable
)

class ErrorRegistry:
    @staticmethod
    def get_error_mappings() -> Dict[Type[Exception], Callable]:
        """Get mappings of exceptions to their handlers."""
        return {
            # MongoDB errors
            mongo_errors.ServerSelectionTimeoutError: lambda e: DatabaseError("MongoDB connection failed", original_error=e),
            mongo_errors.OperationFailure: lambda e: DatabaseError("MongoDB operation failed", original_error=e),
            mongo_errors.ConfigurationError: lambda e: DatabaseError("MongoDB configuration error", original_error=e),
            mongo_errors.NetworkTimeout: lambda e: DatabaseError("MongoDB network timeout", original_error=e),
            
            # YouTube API errors
            NoTranscriptFound: lambda e: ScrapingError("No transcript found", original_error=e),
            TranscriptsDisabled: lambda e: ScrapingError("Transcripts are disabled", original_error=e),
            VideoUnavailable: lambda e: ScrapingError("Video is unavailable", original_error=e),
            
            # Validation errors
            ValueError: lambda e: ValidationError("Validation failed", original_error=e),
            TypeError: lambda e: ValidationError("Type validation failed", original_error=e)
        } 