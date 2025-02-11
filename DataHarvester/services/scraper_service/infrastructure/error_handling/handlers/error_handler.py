# Software/DataHarvester/services/data_ingestion/infrastructure/error_handling/handlers/error_handler.py

from typing import Optional, Dict, Any, Type, Callable, TypeVar, Union, Tuple
import functools
import logging
from pymongo import errors as pymongo_errors
import youtube_transcript_api
import requests
import yaml
from ..exceptions.base import BaseError, ErrorCode, ErrorSeverity
from ..exceptions.specific import *
from infrastructure.logging.logger import get_logger

logger = get_logger()

T = TypeVar('T', bound=Exception)
E = TypeVar('E', bound=BaseError)

class ErrorHandler:
    """Centralized error handling system."""
    
    _error_mappings: Dict[Type[Exception], Callable[[Exception], BaseError]] = {
        # Database errors
        pymongo_errors.ServerSelectionTimeoutError: 
            lambda e: DatabaseError("Database connection failed", original_error=e),
        pymongo_errors.OperationFailure:
            lambda e: DatabaseError("Database operation failed", original_error=e),
            
        # Scraping errors
        youtube_transcript_api.NoTranscriptFound:
            lambda e: ScrapingError("No transcript available", original_error=e),
        youtube_transcript_api.TranscriptsDisabled:
            lambda e: ScrapingError("Transcripts are disabled", original_error=e),
        requests.exceptions.RequestException:
            lambda e: ScrapingError("Network request failed", original_error=e),
            
        # Configuration errors
        yaml.YAMLError:
            lambda e: ConfigurationError("Invalid YAML configuration", ErrorCode.CONFIG_INVALID, original_error=e),
            
        # Default error
        Exception:
            lambda e: BaseError("Unexpected error occurred", ErrorCode.SYSTEM_RESOURCE_ERROR, original_error=e)
    }
    
    @classmethod
    def handle(
        cls,
        error: Exception,
        context: Optional[str] = None,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        details: Optional[Dict[str, Any]] = None
    ) -> BaseError:
        """Handle an exception and convert it to appropriate error type."""
        
        # Find appropriate error mapping
        for error_type, error_factory in cls._error_mappings.items():
            if isinstance(error, error_type):
                custom_error = error_factory(error)
                custom_error.severity = severity  # Set the severity
                break
        else:
            custom_error = cls._error_mappings[Exception](error)
            custom_error.severity = severity  # Set the severity
        
        # Add context and details
        if context:
            custom_error.message = f"[{context}] {custom_error.message}"
        if details:
            custom_error.details.update(details)
        
        # Log the error
        cls._log_error(custom_error)
        
        return custom_error
    
    @staticmethod
    def _log_error(error: BaseError) -> None:
        """Log error with appropriate severity."""
        log_level = {
            ErrorSeverity.DEBUG: logging.DEBUG,
            ErrorSeverity.INFO: logging.INFO,
            ErrorSeverity.WARNING: logging.WARNING,
            ErrorSeverity.ERROR: logging.ERROR,
            ErrorSeverity.CRITICAL: logging.CRITICAL
        }[error.severity]
        
        logger.log(log_level, str(error), extra=error.to_dict())

def handle_errors(error_types: Union[Type[Exception], Tuple[Type[Exception], ...]], 
                 context: Optional[str] = None,
                 severity: ErrorSeverity = ErrorSeverity.ERROR):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except error_types as e:
                error = ErrorHandler.handle(e, context, severity)
                raise error
        return wrapper
    return decorator 