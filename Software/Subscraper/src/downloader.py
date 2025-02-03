import os
import requests
import time
from pathlib import Path
import logging
from requests.exceptions import RequestException, Timeout

class SubtitleDownloader:
    """Handles downloading and organizing subtitle files."""

    def __init__(self, base_path: str = "downloads"):
        """Initialize the downloader with a base path for downloads."""
        self.base_path = Path(base_path)
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging for the downloader."""
        self.logger = logging.getLogger(__name__)

    def _wait_and_retry(self, url: str, max_retries: int = 3) -> requests.Response:
        """Attempt to download with retries and exponential backoff."""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.opensubtitles.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        session = requests.Session()
        
        for attempt in range(max_retries):
            try:
                response = session.get(url, headers=headers, timeout=30)
                response.raise_for_status()
                
                if not response.content:
                    raise ValueError("Empty response received")
                    
                return response
            except (RequestException, Timeout) as e:
                wait_time = (2 ** attempt) + 1
                self.logger.warning(f"Download attempt {attempt + 1} failed: {str(e)}. Waiting {wait_time}s...")
                time.sleep(wait_time)
                
        raise Exception(f"Failed to download after {max_retries} attempts")

    def download_subtitle(self, download_url: str, title: str, 
                        language: str = 'eng', file_name: str | None = None) -> Path:
        """Download a subtitle file and organize it into the appropriate directory."""
        # Create series directory with absolute path
        series_dir = Path(os.path.abspath(self.base_path)) / self._sanitize_filename(title)
        os.makedirs(series_dir, exist_ok=True)
        
        # Ensure directory has correct permissions
        os.chmod(series_dir, 0o777)

        if file_name is None:
            file_name = f"{self._sanitize_filename(title)}_{language}.srt"
        
        output_path = series_dir / file_name
        
        try:
            response = self._wait_and_retry(download_url)
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
                
            self.logger.info(f"Downloaded subtitle to {output_path}")
            return output_path
            
        except (requests.RequestException, Exception) as e:
            self.logger.error(f"Error downloading subtitle: {str(e)}")
            raise

    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """Remove invalid characters from filename."""
        return "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).rstrip() 