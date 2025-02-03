from typing import Dict, Optional
from urllib.parse import urlparse
import re

class OpenSubtitlesURLParser:
    """Parser for OpenSubtitles URLs."""
    
    def __init__(self, url: str):
        self.url = url.strip()
        self.parsed = urlparse(self.url if '://' in self.url else f'https://{self.url}')
        
    def parse(self) -> Dict[str, str]:
        """Parse the URL and extract content information.
        
        Returns:
            Dict containing content type, title, and year if present
        """
        # Extract path components
        path = self.parsed.path.strip('/')
        parts = path.split('/')
        
        # Initialize result
        result = {
            'type': None,
            'title': None,
            'year': None
        }
        
        # Handle different URL formats
        if len(parts) >= 2:
            if 'tvshows' in parts:
                result['type'] = 'episode'
                title_part = parts[-1]
            elif 'movies' in parts:
                result['type'] = 'movie'
                title_part = parts[-1]
            else:
                title_part = parts[-1]
            
            # Extract year and title
            year_match = re.match(r'(\d{4})-(.+)', title_part)
            if year_match:
                result['year'] = year_match.group(1)
                result['title'] = year_match.group(2).replace('-', ' ').strip()
            else:
                result['title'] = title_part.replace('-', ' ').strip()
        
        return result
    
    def get_search_query(self) -> Optional[str]:
        """Convert URL to search query format.
        
        Returns:
            Search query string or None if parsing fails
        """
        info = self.parse()
        if info['title']:
            query = info['title']
            if info['year']:
                query = f"{info['year']} {query}"
            return query
        return None 