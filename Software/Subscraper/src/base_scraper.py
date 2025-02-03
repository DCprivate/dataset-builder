from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path
import logging

class BaseScraper(ABC):
    """Abstract base class for subtitle scrapers."""
    
    def __init__(self):
        self._setup_logging()
        self.download_count = 0
    
    def _setup_logging(self):
        """Configure logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def search(self, query: Optional[str] = None, 
              imdb_id: Optional[str] = None, 
              language: str = 'en', 
              type: str = 'all') -> Dict[str, Any]:
        """Search for subtitles."""
        pass
    
    @abstractmethod
    def download(self, file_id: str) -> Dict[str, str]:
        """Get download information for a subtitle."""
        pass
    
    @property
    def can_download(self) -> bool:
        """Check if the scraper can still download subtitles."""
        return True 