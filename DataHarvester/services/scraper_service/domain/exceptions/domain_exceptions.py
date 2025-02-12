# Software/DataHarvester/services/scraper_service/domain/exceptions/domain_exceptions.py

class YouTubeScraperError(Exception):
    """Base exception class for YouTube Scraper."""
    def __init__(self, message: str, error_code: str | None = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class ConfigurationError(YouTubeScraperError):
    """Raised when there's a configuration error."""
    pass

class DatabaseError(YouTubeScraperError):
    """Raised when there's a database operation error."""
    pass

class ScrapingError(YouTubeScraperError):
    """Raised when there's an error during scraping."""
    pass

class ValidationError(YouTubeScraperError):
    """Raised when there's a validation error."""
    pass

class ProcessingError(YouTubeScraperError):
    """Raised when there's an error during text processing."""
    pass

class NetworkError(YouTubeScraperError):
    """Raised when there's a network-related error."""
    pass 