from typing import Optional, Dict, Any
import os
import requests
from dotenv import load_dotenv
from .base_scraper import BaseScraper

class OpenSubtitlesAPI(BaseScraper):
    """Client for the OpenSubtitles.com REST API."""
    
    BASE_URL = "https://api.opensubtitles.com/api/v1"
    DAILY_DOWNLOAD_LIMIT = 100

    def __init__(self):
        """Initialize the API client with credentials from environment variables."""
        super().__init__()
        load_dotenv()
        self.api_key = os.getenv('API_KEY')
        self.api_name = os.getenv('API_NAME')
        self.token = None
        
        if not self.api_key:
            raise ValueError("API_KEY not found in environment variables")

    def _headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        headers = {
            'Api-Key': self.api_key,
            'User-Agent': f'{self.api_name} v1.0',
            'Content-Type': 'application/json'
        }
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers

    def search(self, query: Optional[str] = None, imdb_id: Optional[str] = None, 
              language: str = 'en', type: str = 'all') -> Dict[str, Any]:
        """Search for subtitles."""
        params = {
            'languages': language,
            'type': type
        }
        
        if query:
            params['query'] = query
        if imdb_id:
            params['imdb_id'] = imdb_id.replace('tt', '')

        response = requests.get(
            f"{self.BASE_URL}/subtitles",
            headers=self._headers(),
            params=params
        )
        response.raise_for_status()
        return response.json()

    def download(self, file_id: str) -> Dict[str, str]:
        """Get download link for a subtitle."""
        if not self.can_download:
            raise ValueError("Daily download limit reached")
            
        response = requests.post(
            f"{self.BASE_URL}/download",
            headers=self._headers(),
            json={'file_id': file_id}
        )
        response.raise_for_status()
        self.download_count += 1
        return response.json()
        
    @property
    def can_download(self) -> bool:
        """Check if we're still under the daily download limit."""
        return self.download_count < self.DAILY_DOWNLOAD_LIMIT 