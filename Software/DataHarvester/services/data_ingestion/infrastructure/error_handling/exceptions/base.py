# src/infrastructure/error_handling/exceptions/base.py

from typing import Optional, Dict, Any
from enum import Enum

class ErrorSeverity(Enum):
    """Severity levels for errors."""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

class ErrorCode(Enum):
    """Centralized error codes."""
    # Database errors (DB)
    DB_CONNECTION_ERROR = "DB001"
    DB_OPERATION_ERROR = "DB002"
    DB_VALIDATION_ERROR = "DB003"
    DATABASE_ERROR = "DB004"
    
    # Configuration errors (CFG)
    CONFIG_MISSING = "CFG001"
    CONFIG_INVALID = "CFG002"
    CONFIG_VALIDATION_ERROR = "CFG003"
    
    # Scraping errors (SCR)
    SCRAPING_NETWORK_ERROR = "SCR001"
    SCRAPING_PARSE_ERROR = "SCR002"
    SCRAPING_RATE_LIMIT = "SCR003"
    SCRAPING_ERROR = "SCR004"
    
    # Processing errors (PRC)
    PROCESSING_ERROR = "PRC001"
    PROCESSING_VALIDATION_ERROR = "PRC002"
    
    # System errors (SYS)
    SYSTEM_RESOURCE_ERROR = "SYS001"
    SYSTEM_DEPENDENCY_ERROR = "SYS002"

    # Validation errors (VAL)
    VALIDATION_ERROR = "VAL001"

class BaseError(Exception):
    """Base exception class for all custom exceptions."""
    
    def __init__(
        self,
        message: str,
        error_code: ErrorCode,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        details: Optional[Dict[str, Any]] = None,
        original_error: Optional[Exception] = None
    ):
        self.message = message
        self.error_code = error_code
        self.severity = severity
        self.details = details or {}
        self.original_error = original_error
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary format."""
        return {
            "error_code": self.error_code.value,
            "message": self.message,
            "severity": self.severity.name,
            "details": self.details,
            "original_error": str(self.original_error) if self.original_error else None
        }
    
    def __str__(self) -> str:
        return f"[{self.error_code.value}] {self.message}" 