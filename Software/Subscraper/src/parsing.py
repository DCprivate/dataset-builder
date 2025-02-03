"""Module for parsing web content and subtitle files."""

from typing import Dict, Any, List
from bs4 import BeautifulSoup
import re

class SubtitleParser:
    """Handles parsing of subtitle content and metadata."""
    
    @staticmethod
    def parse_title(title: str) -> Dict[str, Any]:
        """
        Parse title string to extract season and episode information.
        
        Args:
            title: The title string to parse
            
        Returns:
            Dict containing parsed information
        """
        season_match = re.search(r'[Ss](\d+)[Ee](\d+)', title)
        if season_match:
            return {
                'season': int(season_match.group(1)),
                'episode': int(season_match.group(2))
            }
        return {'season': None, 'episode': None}
    
    @staticmethod
    def parse_subtitle_page(html_content: str) -> List[Dict[str, Any]]:
        """
        Parse the subtitle listing page HTML.
        
        Args:
            html_content: Raw HTML content
            
        Returns:
            List of parsed subtitle entries
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []
        
        for row in soup.select('tr.change'):
            try:
                title_elem = row.select_one('td.name')
                if not title_elem:
                    continue
                    
                title = title_elem.text.strip()
                download_link = row.select_one('a.download-subtitle')
                
                if not download_link:
                    continue
                    
                results.append({
                    'title': title,
                    'download_url': download_link['href'],
                    **SubtitleParser.parse_title(title)
                })
                
            except Exception as e:
                print(f"Error parsing row: {e}")
                continue
                
        return results 