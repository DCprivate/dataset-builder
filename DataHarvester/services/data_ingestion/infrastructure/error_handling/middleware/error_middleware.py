# Software/DataHarvester/services/data_ingestion/infrastructure/error_handling/middleware/error_middleware.py

from functools import wraps
import time
from typing import Callable, Optional, Dict, Any
from infrastructure.logging.logger import get_logger
from infrastructure.config.config_manager import ConfigManager
from infrastructure.error_handling.exceptions.base import BaseError, ErrorSeverity, ErrorCode
from infrastructure.error_handling.utils.time_utils import get_error_timestamp, format_error_duration
from infrastructure.error_handling.utils.text_utils import format_error_message
import logging
from infrastructure.error_handling.error_registry import ErrorRegistry

logger = get_logger()
config = ConfigManager().get_config('harvesting')

class ErrorMiddleware:
    """Centralized error handling and middleware system."""
    
    _error_mappings = ErrorRegistry.get_error_mappings()

    class RateLimiter:
        def __init__(self):
            self.last_request_time = 0
            self.delay = config['scraping']['delay_between_requests']

        def wait(self):
            """Wait appropriate time between requests."""
            current_time = time.time()
            time_since_last = current_time - self.last_request_time
            if time_since_last < self.delay:
                time.sleep(self.delay - time_since_last)
            self.last_request_time = time.time()

    @classmethod
    def handle_error(
        cls,
        error: Exception,
        context: Optional[str] = None,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        details: Optional[Dict[str, Any]] = None
    ) -> BaseError:
        """Central error handling logic."""
        error_type = type(error)
        
        # Find appropriate error mapping
        error_factory = cls._error_mappings.get(
            error_type,
            lambda e: BaseError("Unexpected error", ErrorCode.SYSTEM_RESOURCE_ERROR, original_error=e)
        )
        
        # Create error instance with specified severity
        custom_error = error_factory(error)
        custom_error.severity = severity  # Set the severity level
        
        # Add context and details
        if context:
            custom_error.message = format_error_message(custom_error.message, context)
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

    @staticmethod
    def rate_limit(func: Callable) -> Callable:
        """Decorator to apply rate limiting with error handling."""
        limiter = ErrorMiddleware.RateLimiter()
        
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            limiter.wait()
            return func(*args, **kwargs)
        return wrapper
    
    @classmethod
    def catch_errors(
        cls,
        error_types: Optional[tuple] = None,
        context: Optional[str] = None,
        severity: ErrorSeverity = ErrorSeverity.ERROR
    ) -> Callable:
        """Decorator to catch and handle specific error types."""
        if error_types is None:
            error_types = (Exception,)

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                try:
                    return func(*args, **kwargs)
                except error_types as e:
                    error = cls.handle_error(
                        error=e,
                        context=context,
                        severity=severity,
                        details={
                            "timestamp": get_error_timestamp(),
                            "function": func.__name__,
                            "args": str(args),
                            "kwargs": str(kwargs)
                        }
                    )
                    raise error
            return wrapper
        return decorator

    @classmethod
    def log_errors(
        cls,
        error_types: Optional[tuple] = None,
        reraise: bool = True
    ) -> Callable:
        """Decorator to log errors without handling them."""
        if error_types is None:
            error_types = (Exception,)

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                try:
                    return func(*args, **kwargs)
                except error_types as e:
                    cls._log_error(cls.handle_error(e))
                    if reraise:
                        raise
            return wrapper
        return decorator 

    @classmethod
    def retry(
        cls,
        retries: Optional[int] = None,
        delay: Optional[float] = None,
        exceptions: tuple = (Exception,),
        exponential_backoff: bool = True,
        max_delay: int = 300,
        context: Optional[str] = None
    ) -> Callable:
        """Decorator for retrying operations with exponential backoff."""
        if retries is None:
            retries = config['scraping']['max_retries']
        if delay is None:
            delay = config['scraping']['retry_delay']

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            @cls.catch_errors(error_types=exceptions, context=context)
            def wrapper(*args, **kwargs) -> Any:
                last_error = None
                retry_count = retries if retries is not None else config['scraping']['max_retries']
                for attempt in range(retry_count):
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        last_error = e
                        if attempt == retry_count - 1:
                            logger.error(
                                f"Operation failed after {retry_count} attempts: {str(e)}",
                                extra={"function": func.__name__, "attempt": attempt + 1}
                            )
                            raise cls.handle_error(
                                error=last_error,
                                context=f"{context or func.__name__} (Retry Exhausted)",
                                details={
                                    "attempts": retry_count,
                                    "last_error": str(last_error)
                                }
                            )
                        
                        base_delay = delay if delay is not None else config['scraping']['retry_delay']
                        wait_time = base_delay * (2 ** attempt if exponential_backoff else 1)
                        wait_time = min(wait_time, max_delay)
                        
                        logger.warning(
                            f"Attempt {attempt + 1}/{retry_count} failed: {str(e)}, "
                            f"retrying in {format_error_duration(wait_time)}...",
                            extra={"function": func.__name__, "attempt": attempt + 1}
                        )
                        time.sleep(wait_time)
                return None
            return wrapper
        return decorator

    @classmethod
    def with_retry_and_rate_limit(
        cls,
        retries: Optional[int] = None,
        delay: Optional[float] = None,
        exceptions: tuple = (Exception,),
        context: Optional[str] = None
    ) -> Callable:
        """Convenience decorator combining retry and rate limiting."""
        def decorator(func: Callable) -> Callable:
            @cls.retry(
                retries=retries,
                delay=delay,
                exceptions=exceptions,
                context=context
            )
            @cls.rate_limit
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                return func(*args, **kwargs)
            return wrapper
        return decorator 

    @staticmethod
    def catch_async_errors(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}")
                raise
        return wrapper 