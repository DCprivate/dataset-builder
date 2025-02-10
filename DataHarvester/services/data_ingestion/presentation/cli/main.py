# Software/DataHarvester/services/data_ingestion/presentation/cli/main.py

import logging
import yaml
import time
from application.services.transcript.transcript_processor import VideoProcessor
from infrastructure.monitoring.health_checker import HealthChecker
from infrastructure.logging.logger import get_logger
from infrastructure.config.config_manager import ConfigManager
from infrastructure.persistence.mongodb.mongo_repository import MongoDBClient

# Initialize logger at module level
logger = get_logger()

def load_urls(config_file: str = "config/urls.yaml") -> dict:
    """Load URLs from configuration file."""
    default_config = {
        "urls": {
            "videos": [],
            "playlists": [],
            "channels": []
        },
        "config": {
            "delay_between_videos": 2
        }
    }
    
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
            if not config:
                return default_config
            # Ensure all required keys exist
            if "urls" not in config:
                config["urls"] = default_config["urls"]
            if "config" not in config:
                config["config"] = default_config["config"]
            return config
    except Exception as e:
        logging.error(f"Error loading URLs config: {e}")
        return default_config

def process_playlist_videos(processor: VideoProcessor, playlist_url: str, delay: int) -> None:
    """Process all videos in a playlist."""
    try:
        # Extract video URLs from playlist
        video_urls = processor.extractor.get_playlist_video_urls(playlist_url)
        
        for video_url in video_urls:
            try:
                logging.info(f"Processing video from playlist: {video_url}")
                success = processor.process_video(video_url)
                if not success:
                    logging.warning(f"Failed to process video from playlist: {video_url}")
                time.sleep(delay)
            except Exception as e:
                logging.error(f"Error processing playlist video {video_url}: {str(e)}")
                continue
    except Exception as e:
        logging.error(f"Error processing playlist {playlist_url}: {str(e)}")

def process_channel_videos(processor: VideoProcessor, channel_url: str, delay: int) -> None:
    """Process all videos in a channel."""
    try:
        # Convert channel URL to playlist URL of all videos
        channel_playlist_url = f"{channel_url}/videos"
        video_urls = processor.extractor.get_playlist_video_urls(channel_playlist_url)
        
        for video_url in video_urls:
            try:
                logging.info(f"Processing video from channel: {video_url}")
                success = processor.process_video(video_url)
                if not success:
                    logging.warning(f"Failed to process video from channel: {video_url}")
                time.sleep(delay)
            except Exception as e:
                logging.error(f"Error processing channel video {video_url}: {str(e)}")
                continue
    except Exception as e:
        logging.error(f"Error processing channel {channel_url}: {str(e)}")

def setup_logging():
    """Configure logging settings."""
    # Remove the existing logging setup and use the dedicated logger
    global logger
    logger = get_logger()
    
    # Reduce noise from specific loggers
    logging.getLogger('presidio-analyzer').setLevel(logging.WARNING)
    logging.getLogger('presidio-anonymizer').setLevel(logging.WARNING)
    logging.getLogger('spacy').setLevel(logging.WARNING)

async def main():
    try:
        # Load configurations
        config = ConfigManager()
        db_config = config.get_config('database')
        sources_config = config.get_config('sources')
        
        # Initialize MongoDB client
        mongo_client = await MongoDBClient.create(
            mongo_uri=db_config.get('mongodb', {}).get('uri', 'mongodb://mongo:27017/')
        )
        
        # Perform health checks
        logger.info("Starting system health checks...")
        health_checker = HealthChecker()
        health_checker.check_all()
        
        # Initialize video processor
        processor = VideoProcessor()
        
        # Process videos from sources config
        videos = sources_config.get('sources', {}).get('videos', [])
        for video_url in videos:
            processor.process_video(video_url)
            
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise
    finally:
        if mongo_client:
            await mongo_client.cleanup()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 