# Software/DataHarvester/services/scraper_service/application/services/transcript/transcript_fetcher.py

from typing import List
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from pytube import Playlist

from infrastructure.logging.logger import get_logger
from infrastructure.config.config_manager import ConfigManager
from infrastructure.error_handling.exceptions.base import ErrorCode, ErrorSeverity
from infrastructure.error_handling.exceptions.specific import ScrapingError
from infrastructure.error_handling.handlers.error_handler import handle_errors
from infrastructure.error_handling.middleware.error_middleware import ErrorMiddleware

logger = get_logger()
config = ConfigManager().get_config('scraping')

class TranscriptFetcher:
    def __init__(self):
        self.preferred_languages = config['scraping']['preferred_languages']
        self.fallback_to_auto_translate = config['scraping']['fallback_to_auto_translate']
        self.include_auto_generated = config['scraping']['include_auto_generated']
        self.config = ConfigManager().get_config('harvesting')
        self.transcript_api = YouTubeTranscriptApi()

    @staticmethod
    @handle_errors(
        ValueError,
        context="URL Parsing",
        severity=ErrorSeverity.ERROR
    )
    def extract_video_id(url: str) -> str:
        """Extract video ID from YouTube URL."""
        if "youtube.com/watch?v=" in url:
            return url.split("watch?v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0]
        raise ValueError(f"Invalid YouTube URL format: {url}")

    @ErrorMiddleware.retry()
    @handle_errors(
        (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable),
        context="Transcript Processing",
        severity=ErrorSeverity.ERROR
    )
    def get_transcripts(self, video_id: str) -> List[dict]:
        """Extract transcript from a YouTube video."""
        try:
            transcript_list = self.transcript_api.list_transcripts(video_id)
            
            # Try to get preferred language transcript
            for lang in self.preferred_languages:
                try:
                    transcript = transcript_list.find_transcript([lang])
                    return transcript.fetch()
                except NoTranscriptFound:
                    continue

            # Fallback to auto-translated if enabled
            if self.fallback_to_auto_translate:
                try:
                    transcript = transcript_list.find_transcript(
                        self.preferred_languages
                    ).translate(self.preferred_languages[0])
                    return transcript.fetch()
                except Exception as e:
                    raise ScrapingError(
                        "Failed to get auto-translated transcript",
                        ErrorCode.SCRAPING_PARSE_ERROR,
                        ErrorSeverity.ERROR, # type: ignore
                        details={"video_id": video_id},
                        original_error=e
                    )

            raise NoTranscriptFound(video_id=video_id, requested_language_codes=self.preferred_languages, transcript_data=transcript_list)
            
        except Exception as e:
            raise ScrapingError(
                "Failed to extract transcript",
                ErrorCode.SCRAPING_PARSE_ERROR,
                ErrorSeverity.ERROR, # type: ignore
                details={"video_id": video_id},
                original_error=e
            )

    @ErrorMiddleware.retry()
    @handle_errors(Exception, context="Playlist Extraction")
    def get_playlist_video_urls(self, playlist_url: str) -> List[str]:
        """Extract all video URLs from a playlist or channel."""
        try:
            playlist = Playlist(playlist_url)
            urls = list(playlist.video_urls)  # Force playlist to load by converting iterator to list
            
            if not urls:
                logger.warning(f"No videos found in playlist: {playlist_url}")
                
            return urls
            
        except Exception as e:
            raise ScrapingError(
                "Failed to extract videos from playlist",
                ErrorCode.SCRAPING_PARSE_ERROR,
                ErrorSeverity.ERROR, # type: ignore
                details={"playlist_url": playlist_url},
                original_error=e
            ) 