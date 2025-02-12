# Software/DataHarvester/services/scraper_service/application/services/transcript/transcript_processor.py
from typing import List, Dict, Any
from celery import Celery
from infrastructure.config.config_manager import ConfigManager
from infrastructure.logging.logger import get_logger
from infrastructure.error_handling.middleware.error_middleware import ErrorMiddleware
from .transcript_service import TranscriptFetcher
from ..text.text_cleaner_service import TranscriptCleaner
from infrastructure.redis.producer import ScraperProducer
from domain.models.transcript import ProcessedTranscript as TranscriptModel
from datetime import datetime, timezone

# Initialize Celery with Redis backend
celery_app = Celery('transcript_tasks',
                   broker='redis://redis:6379/0',
                   backend='redis://redis:6379/0')

logger = get_logger()

@celery_app.task(name='transcript.process_video')
def process_video_task(video_url: str) -> Dict[str, Any]:
    """Process a single video transcript and queue for storage."""
    processor = VideoProcessor()
    result = processor.process_single_video(video_url)
    return result

@celery_app.task(name='transcript.process_batch')
def process_batch_task(video_urls: List[str]) -> List[Dict[str, Any]]:
    """Process a batch of video transcripts."""
    results = []
    for url in video_urls:
        result = process_video_task.delay(url)
        results.append(result)
    return results

class VideoProcessor:
    def __init__(self):
        self.config = ConfigManager()
        self.batch_size = self.config.get_config('harvesting').get('batch_size', 10)
        self.sources = self.config.get_config('harvesting').get('sources', {})
        self.extractor = TranscriptFetcher()
        self.cleaner = TranscriptCleaner()
        self.producer = ScraperProducer()

    @ErrorMiddleware.catch_async_errors
    def process_single_video(self, video_url: str) -> Dict[str, Any]:
        """Process a single video transcript."""
        try:
            video_id = self.extractor.extract_video_id(video_url)
            if not video_id:
                logger.error(f"Could not extract video ID from {video_url}")
                return {'success': False, 'video_url': video_url, 'error': 'Invalid video ID'}

            transcripts = self.extractor.get_transcripts(video_id)
            if not transcripts:
                logger.warning(f"No transcripts found for video {video_id}")
                return {'success': False, 'video_url': video_url, 'error': 'No transcripts found'}

            # Clean transcripts
            cleaned_transcripts = [
                self.cleaner.clean_text(transcript['text'])
                for transcript in transcripts
            ]

            # Queue for worker processing
            celery_app.send_task(
                'worker.store_transcript',
                args=[{
                    'video_id': video_id,
                    'transcripts': cleaned_transcripts,
                    'processed': False
                }],
                queue='storage'
            )
            logger.info(f"Successfully queued video {video_id} for storage")
            return {
                'success': True,
                'video_id': video_id,
                'transcript_count': len(cleaned_transcripts)
            }

        except Exception as e:
            logger.error(f"Error processing video {video_url}: {str(e)}")
            return {'success': False, 'video_url': video_url, 'error': str(e)}

    @ErrorMiddleware.catch_async_errors
    def process_batch(self, video_urls: List[str]) -> None:
        """Process a batch of videos."""
        for i in range(0, len(video_urls), self.batch_size):
            batch = video_urls[i:i + self.batch_size]
            process_batch_task.delay(batch)
            logger.info(f"Submitted batch {i//self.batch_size + 1} for processing")

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
        """Process all configured videos in batches."""
        videos = self.get_video_urls()
        playlists = self.get_playlist_urls()
        channels = self.get_channel_urls()
        
        logger.info(f"Found {len(videos)} videos, {len(playlists)} playlists, and {len(channels)} channels to process")
        
        # Process in batches
        batch_size = self.batch_size
        for i in range(0, len(videos), batch_size):
            batch = videos[i:i + batch_size]
            process_batch_task.delay(batch)
            logger.info(f"Submitted batch {i//batch_size + 1} for processing")

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
        
            return True

        except Exception as e:
            logger.error(f"Error processing video {video_url}: {str(e)}")
            return False

    async def process_transcript(self, video_url: str, transcript_data: Dict[str, Any]) -> bool:
        """Process transcript and send to queue"""
        try:
            # Create transcript model
            transcript = TranscriptModel(
                video_id=video_url.split("=")[-1],
                channel_id=transcript_data.get("channel_id"),
                full_text=transcript_data.get("content", ""),
                metadata=transcript_data.get("metadata", {}),
                word_count=len(transcript_data.get("content", "").split()),
                language=transcript_data.get("language", "en"),
                processing_stats={"processed_at": datetime.now(timezone.utc).isoformat()}
            )
            
            # Send to Redis queue
            success = self.producer.send_to_queue(
                content=transcript.full_text,
                metadata={
                    "video_id": transcript.video_id,
                    "language": transcript.language,
                    **transcript.metadata
                }
            )
            
            if not success:
                logger.error(f"Failed to queue transcript for {video_url}")
                return False
                
            logger.info(f"Successfully queued transcript for {video_url}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing transcript for {video_url}: {str(e)}")
            return False
            
    def __del__(self):
        """Cleanup Redis connection"""
        self.producer.close() 