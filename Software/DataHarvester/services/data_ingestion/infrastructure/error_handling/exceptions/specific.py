# Software/DataHarvester/src/infrastructure/error_handling/exceptions/specific.py

from typing import Optional, Dict, Any
from .base import BaseError, ErrorCode, ErrorSeverity

class DatabaseError(BaseError):
    """Database-related errors."""
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.DATABASE_ERROR,
            severity=ErrorSeverity.ERROR,
            original_error=original_error
        )

class ConfigurationError(BaseError):
    """Configuration-related errors."""
    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.CONFIG_INVALID,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        details: Optional[Dict[str, Any]] = None,
        original_error: Optional[Exception] = None
    ):
        super().__init__(message, error_code, severity, details, original_error)

class ScrapingError(BaseError):
    """Scraping-related errors."""
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.SCRAPING_ERROR,
            severity=ErrorSeverity.ERROR,
            original_error=original_error
        )

class ProcessingError(BaseError):
    """Data processing-related errors."""
    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.PROCESSING_ERROR,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        details: Optional[Dict[str, Any]] = None,
        original_error: Optional[Exception] = None
    ):
        super().__init__(message, error_code, severity, details, original_error)

class SystemError(BaseError):
    """System-level errors."""
    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.SYSTEM_RESOURCE_ERROR,
        severity: ErrorSeverity = ErrorSeverity.CRITICAL,
        details: Optional[Dict[str, Any]] = None,
        original_error: Optional[Exception] = None
    ):
        super().__init__(message, error_code, severity, details, original_error)

class ValidationError(BaseError):
    """Validation-related errors."""
    def __init__(self, message: str, original_error: Optional[Exception] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.VALIDATION_ERROR,
            severity=ErrorSeverity.ERROR,
            original_error=original_error,
            details=details
        ) 