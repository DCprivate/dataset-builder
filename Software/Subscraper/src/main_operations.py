"""Module containing main scraping operations."""

from typing import Dict, Any, Optional
import logging
from .web_scraper import OpenSubtitlesWebScraper
from .downloader import SubtitleDownloader

logger = logging.getLogger(__name__)

class MainOperations:
    """Handles high-level scraping operations."""
    
    def __init__(self):
        self.scraper = OpenSubtitlesWebScraper()
        self.downloader = SubtitleDownloader()
        
    def search_and_download(self, 
                          url: str, 
                          language: str = 'en',
                          max_results: Optional[int] = None) -> Dict[str, Any]:
        """
        Search for subtitles and download them.
        
        Args:
            url: The URL to search
            language: Language code for subtitles
            max_results: Maximum number of results to process
            
        Returns:
            Dict containing operation results
        """
        try:
            results = self.scraper.search(url=url, language=language)
            
            if not results.get('data'):
                logger.warning("No subtitles found")
                return {'success': False, 'message': 'No subtitles found'}
                
            downloaded = []
            for idx, result in enumerate(results['data'][:max_results]):
                try:
                    subtitle = self.downloader.download_subtitle(
                        download_url=result['download_url'],
                        title=result['attributes']['feature_details']['title'],
                        language=language
                    )
                    downloaded.append(subtitle)
                except Exception as e:
                    logger.error(f"Error downloading subtitle: {str(e)}")
                    
            return {
                'success': True,
                'downloaded': downloaded,
                'total': len(downloaded)
            }
            
        except Exception as e:
            logger.error(f"Operation failed: {str(e)}")
            return {'success': False, 'message': str(e)} 