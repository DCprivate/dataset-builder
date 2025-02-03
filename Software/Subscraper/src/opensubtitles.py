#!/usr/bin/env python3

from typing import Dict, Any, List
from urllib.parse import urlparse
import logging
from .element_locations import ElementLocations
from .parsing import SubtitleParser
from .main_operations import MainOperations
from .exceptions import InvalidURLError, DownloadError

logger = logging.getLogger(__name__)

class OpenSubtitlesAPI:
    """Handles interaction with OpenSubtitles API."""
    
    def __init__(self):
        """Initialize the OpenSubtitles API handler."""
        try:
            self.operations = MainOperations()
            self.parser = SubtitleParser()
        except Exception as e:
            logger.error(f"Failed to initialize OpenSubtitlesAPI: {str(e)}")
            raise
            
    def _validate_url(self, url: str) -> bool:
        """Validate URL format."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
            
    def search_subtitles(self, url: str, language: str = 'en') -> Dict[str, List[Dict]]:
        """
        Search for subtitles using the provided URL.
        
        Args:
            url: The URL to search
            language: Language code for subtitles
            
        Returns:
            Dict containing search results with subtitle metadata
            
        Raises:
            InvalidURLError: If URL is invalid
            ConnectionError: If search fails
        """
        if not self._validate_url(url):
            raise InvalidURLError(f"Invalid URL provided: {url}")
            
        try:
            results = self.operations.search_and_download(
                url=url,
                language=language
            )
            return results
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            raise
            
    def download_subtitle(self, download_url: str, title: str, language: str = 'en') -> str:
        """
        Download a specific subtitle.
        
        Args:
            download_url: Direct URL to subtitle
            title: Title of the media
            language: Language code for subtitle
            
        Returns:
            Path to downloaded subtitle file
            
        Raises:
            InvalidURLError: If URL is invalid
            DownloadError: If download fails
        """
        if not self._validate_url(download_url):
            raise InvalidURLError(f"Invalid download URL: {download_url}")
            
        try:
            return self.operations.download_subtitle(
                download_url=download_url,
                title=title,
                language=language
            )
        except Exception as e:
            logger.error(f"Download failed: {str(e)}")
            raise DownloadError(f"Failed to download subtitle: {str(e)}")