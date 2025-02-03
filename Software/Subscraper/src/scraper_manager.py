from typing import Optional, Dict, Any
from .api_client import OpenSubtitlesAPI
from .web_scraper import OpenSubtitlesWebScraper

class ScraperManager:
    """Manages both API and web scraping approaches."""
    
    def __init__(self):
        """Initialize both scrapers."""
        self.api_scraper = OpenSubtitlesAPI()
        self.web_scraper = OpenSubtitlesWebScraper()
        self.current_scraper = self.api_scraper
        
    def _switch_to_web_scraper(self):
        """Switch from API to web scraper when API limit is reached."""
        self.current_scraper = self.web_scraper
        
    def search(self, query: Optional[str] = None, imdb_id: Optional[str] = None, 
              language: str = 'en', type: str = 'all') -> Dict[str, Any]:
        """Search for subtitles using current scraper."""
        return self.current_scraper.search(
            query=query,
            imdb_id=imdb_id,
            language=language,
            type=type
        )
        
    def download(self, file_id: str) -> Dict[str, str]:
        """Download subtitle using current scraper."""
        try:
            if not self.current_scraper.can_download:
                self._switch_to_web_scraper()
                
            return self.current_scraper.download(file_id)
            
        except Exception as e:
            if isinstance(self.current_scraper, OpenSubtitlesAPI):
                self._switch_to_web_scraper()
                return self.current_scraper.download(file_id)
            raise e 