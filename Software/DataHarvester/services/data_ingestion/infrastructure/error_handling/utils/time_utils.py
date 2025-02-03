# Software/DataHarvester/src/infrastructure/error_handling/utils/time_utils.py

from datetime import datetime, timezone
from typing import Union

def get_error_timestamp() -> float:
    """Get current UTC timestamp for error logging."""
    return datetime.now(timezone.utc).timestamp()

def format_error_duration(seconds: Union[int, float]) -> str:
    """Format error duration in seconds to human-readable string."""
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    
    return " ".join(parts) 