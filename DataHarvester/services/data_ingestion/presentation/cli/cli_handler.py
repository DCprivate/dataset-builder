# Software/DataHarvester/services/data_ingestion/presentation/cli/cli_handler.py

import logging
import yaml
import time
from application.services.transcript.transcript_processor import VideoProcessor
from infrastructure.monitoring.health_checker import HealthChecker
from infrastructure.logging.logger import get_logger
from infrastructure.config.config_manager import ConfigManager

logger = get_logger()

def load_urls(config_file: str = "config/urls.yaml") -> dict:
    """Load URLs from configuration file with proper error handling."""
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
            config["urls"] = config.get("urls", default_config["urls"])
            config["config"] = config.get("config", default_config["config"])
            return config
    except Exception as e:
        logger.error(f"Error loading URLs config: {e}")
        return default_config

def process_playlist_videos(processor: VideoProcessor, playlist_url: str, delay: int) -> None:
    """Process all videos in a playlist with error handling."""
    try:
        video_urls = processor.extractor.get_playlist_video_urls(playlist_url)
        
        for video_url in video_urls:
            try:
                logger.info(f"Processing video from playlist: {video_url}")
                processor.process_single_video(video_url)
                time.sleep(delay)
            except Exception as e:
                logger.error(f"Error processing playlist video {video_url}: {str(e)}")
    except Exception as e:
        logger.error(f"Error processing playlist {playlist_url}: {str(e)}")

def process_channel_videos(processor: VideoProcessor, channel_url: str, delay: int) -> None:
    """Process all videos in a channel with error handling."""
    try:
        channel_playlist_url = f"{channel_url}/videos"
        video_urls = processor.extractor.get_playlist_video_urls(channel_playlist_url)
        
        for video_url in video_urls:
            try:
                logger.info(f"Processing video from channel: {video_url}")
                processor.process_single_video(video_url)
                time.sleep(delay)
            except Exception as e:
                logger.error(f"Error processing channel video {video_url}: {str(e)}")
    except Exception as e:
        logger.error(f"Error processing channel {channel_url}: {str(e)}")

def setup_logging():
    """Configure logging settings with third-party library adjustments."""
    global logger
    logger = get_logger()
    
    # Reduce noise from specific loggers
    logging.getLogger('presidio-analyzer').setLevel(logging.WARNING)
    logging.getLogger('presidio-anonymizer').setLevel(logging.WARNING)
    logging.getLogger('spacy').setLevel(logging.WARNING)

def main():
    """Main entry point for CLI execution."""
    try:
        config = ConfigManager()
        sources_config = config.get_config('sources')
        processing_config = load_urls().get('config', {})
        delay = processing_config.get('delay_between_videos', 2)
        
        logger.info("Starting system health checks...")
        HealthChecker().check_all()
        
        processor = VideoProcessor()
        
        # Process individual videos
        for video_url in sources_config.get('videos', []):
            processor.process_single_video(video_url)
            time.sleep(delay)
        
        # Process playlists
        for playlist_url in sources_config.get('playlists', []):
            process_playlist_videos(processor, playlist_url, delay)
        
        # Process channels
        for channel_url in sources_config.get('channels', []):
            process_channel_videos(processor, channel_url, delay)
            
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    setup_logging()
    main()
