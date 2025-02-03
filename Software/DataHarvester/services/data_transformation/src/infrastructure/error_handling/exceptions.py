from enum import Enum
from typing import Optional, Dict, Any

class ErrorSeverity(Enum):
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class ErrorCode(Enum):
    LLM_ERROR = "LLM_ERROR"

class LLMError(Exception):
    def __init__(
        self, 
        message: str,
        error_code: ErrorCode,
        severity: ErrorSeverity,
        details: Optional[Dict[str, Any]] = None,
        original_error: Optional[Exception] = None
    ):
        self.message = message
        self.error_code = error_code
        self.severity = severity
        self.details = details or {}
        self.original_error = original_error
        super().__init__(message)