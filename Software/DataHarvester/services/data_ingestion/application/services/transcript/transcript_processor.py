# Software/DataHarvester/src/services/transcript/processor.py

from typing import List
from infrastructure.config.config_manager import ConfigManager
from infrastructure.logging.logger import get_logger
from infrastructure.persistence.mongodb.mongo_repository import MongoDBClient
from infrastructure.error_handling.middleware.error_middleware import ErrorMiddleware
from application.services.transcript.transcript_service import TranscriptFetcher
from application.services.text.text_cleaner_service import TranscriptCleaner

logger = get_logger()

class VideoProcessor:
    def __init__(self, mongo_uri: str | None = None):
        self.config = ConfigManager()
        self.sources = self.config.get_config('sources')
        self.harvesting_config = self.config.get_config('harvesting')
        self.cleaning_config = self.config.get_config('cleaning')
        
        # Initialize MongoDB client
        if mongo_uri:
            self.db = MongoDBClient(mongo_uri=mongo_uri)
        else:
            db_config = self.config.get_config('database')
            self.db = MongoDBClient(mongo_uri=db_config.get('mongodb', {}).get('uri'))
        
        # Initialize components
        self.extractor = TranscriptFetcher()
        self.cleaner = TranscriptCleaner()
        
        # Get processing settings
        processing_config = self.harvesting_config.get('processing', {})
        self.batch_size = processing_config.get('batch_size', 100)
        self.max_workers = processing_config.get('max_workers', 4)
        
        logger.info(f"VideoProcessor initialized with MongoDB: {self.db.database_name}")

    def get_video_urls(self) -> List[str]:
        """Get list of video URLs to process."""
        try:
            return self.sources.get('sources', {}).get('videos', [])
        except Exception as e:
            logger.error(f"Error getting video URLs: {str(e)}")
            return []

    def get_playlist_urls(self) -> List[str]:
        """Get list of playlist URLs to process."""
        try:
            return self.sources.get('sources', {}).get('playlists', [])
        except Exception as e:
            logger.error(f"Error getting playlist URLs: {str(e)}")
            return []

    def get_channel_urls(self) -> List[str]:
        """Get list of channel URLs to process."""
        try:
            return self.sources.get('sources', {}).get('channels', [])
        except Exception as e:
            logger.error(f"Error getting channel URLs: {str(e)}")
            return []

    @ErrorMiddleware.catch_async_errors
    async def process_videos(self):
        """Process all configured videos."""
        videos = self.get_video_urls()
        playlists = self.get_playlist_urls()
        channels = self.get_channel_urls()
        
        logger.info(f"Found {len(videos)} videos, {len(playlists)} playlists, and {len(channels)} channels to process")
        
        # TODO: Implement video processing logic
        pass

    def process_video(self, video_url: str) -> bool:
        try:
            # Extract video ID
            video_id = self.extractor.extract_video_id(video_url)
            if not video_id:
                logger.error(f"Could not extract video ID from {video_url}")
                return False

            # Get transcripts
            transcripts = self.extractor.get_transcripts(video_id)
            if not transcripts:
                logger.warning(f"No transcripts found for video {video_id}")
                return False

            # Debug log the structure of transcripts
            logger.info(f"Raw transcript structure: {type(transcripts)}")
            if transcripts:
                logger.info(f"First transcript entry: {transcripts[0]}")

            # Clean the transcripts while preserving timing information
            cleaned_transcripts = []
            for transcript in transcripts:
                if not isinstance(transcript, dict):
                    logger.warning(f"Unexpected transcript format: {type(transcript)}")
                    continue
                    
                if 'text' not in transcript:
                    logger.warning("Transcript missing text field")
                    continue

                # Clean the text
                original_text = transcript['text']
                cleaned_text = self.cleaner.clean_transcript([original_text])
                
                # Debug log the cleaning results
                logger.info(f"Original text: {original_text}")
                logger.info(f"Cleaned text: {cleaned_text}")

                if cleaned_text:  # Only add if we have cleaned text
                    cleaned_transcripts.append({
                        'text': cleaned_text,
                        'start': transcript.get('start', 0),
                        'duration': transcript.get('duration', 0)
                    })

            if not cleaned_transcripts:
                logger.warning(f"No cleaned transcripts produced for video {video_id}")
                return False

            # Debug log the final structure
            logger.info(f"Final cleaned transcripts count: {len(cleaned_transcripts)}")
            if cleaned_transcripts:
                logger.info(f"First cleaned transcript: {cleaned_transcripts[0]}")
                
            # Store in database
            self.db.store_video(video_id, cleaned_transcripts)
            logger.info(f"Successfully stored video {video_id} in database")
            return True

        except Exception as e:
            logger.error(f"Error processing video {video_url}: {str(e)}")
            return False 