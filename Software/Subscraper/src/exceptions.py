"""Custom exceptions for the subtitle scraper."""

class SubtitleScraperError(Exception):
    """Base exception class for subtitle scraper."""
    pass

class InvalidURLError(SubtitleScraperError):
    """Raised when an invalid URL is provided."""
    pass

class DownloadError(SubtitleScraperError):
    """Raised when subtitle download fails."""
    pass 