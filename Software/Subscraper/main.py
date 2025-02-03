#!/usr/bin/env python3

import argparse
import logging
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

from src.url_parser import OpenSubtitlesURLParser
from src.scraper_manager import ScraperManager
from src.downloader import SubtitleDownloader

def setup_logging(log_level: str = 'INFO') -> logging.Logger:
    """Configure logging for the application."""
    log_dir = os.environ.get('LOG_DIR', '/app/logs')
    log_file = os.path.join(log_dir, 'subscraper.log')
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file)
        ]
    )
    return logging.getLogger(__name__)

def parse_args() -> argparse.Namespace:
    """Parse and validate command line arguments."""
    parser = argparse.ArgumentParser(
        description='Download subtitles using OpenSubtitles API with web scraping fallback'
    )
    
    # Content identification group
    content_group = parser.add_mutually_exclusive_group(required=True)
    content_group.add_argument(
        '--url',
        type=str,
        help='OpenSubtitles URL (e.g., www.opensubtitles.com/en/tvshows/2018-bluey)'
    )
    content_group.add_argument(
        '--query',
        type=str,
        help='Search query (e.g., "Bluey 2018")'
    )
    content_group.add_argument(
        '--imdb_id',
        type=str,
        help='IMDb ID (with or without tt prefix)'
    )
    
    # Add season/episode options for TV shows
    parser.add_argument(
        '--season',
        type=int,
        help='Season number (for TV shows)'
    )
    parser.add_argument(
        '--episode',
        type=int,
        help='Episode number (for TV shows)'
    )
    
    # Filter arguments
    parser.add_argument(
        '--language',
        type=str,
        default='en',
        help='Subtitle language code (default: en)'
    )
    parser.add_argument(
        '--type',
        type=str,
        default='all',
        choices=['movie', 'episode', 'all'],
        help='Type of content to search for'
    )
    
    # Output arguments
    parser.add_argument(
        '--output_dir',
        type=str,
        default='downloads',
        help='Base directory for downloaded subtitles'
    )
    parser.add_argument(
        '--log_level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level'
    )

    args = parser.parse_args()
    
    # Process URL if provided
    if args.url:
        url_parser = OpenSubtitlesURLParser(args.url)
        query = url_parser.get_search_query()
        if not query:
            parser.error("Could not parse URL. Please check the format.")
        args.query = query
        
        # Set content type if detected from URL
        info = url_parser.parse()
        if info['type']:
            args.type = info['type']
    
    return args

def validate_environment() -> bool:
    """Validate environment setup."""
    env_path = Path('.env')
    if not env_path.exists():
        print("Error: .env file not found")
        return False
    
    load_dotenv(env_path)
    required_vars = ['API_KEY', 'API_NAME']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Error: Missing environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file")
        return False
    return True

def main() -> int:
    """Main execution function."""
    # Parse arguments
    args = parse_args()
    
    # Setup logging
    logger = setup_logging(args.log_level)
    logger.debug("Starting subscraper with arguments: %s", args)
    
    # Validate environment
    if not validate_environment():
        return 1
    
    try:
        # Initialize scraper and downloader
        scraper = ScraperManager()
        downloader = SubtitleDownloader(base_path=args.output_dir)
        
        # Search for subtitles
        logger.info("Searching for subtitles...")
        search_params = {
            'query': args.query,
            'imdb_id': args.imdb_id,
            'language': args.language,
            'type': args.type
        }
        
        if args.season is not None:
            search_params['season_number'] = args.season
        if args.episode is not None:
            search_params['episode_number'] = args.episode
            
        results = scraper.search(**search_params)
        
        if not results.get('data'):
            logger.error("No subtitles found")
            return 1
        
        # Process each result
        success_count = 0
        total_count = len(results['data'])
        
        for idx, item in enumerate(results['data'], 1):
            try:
                title = item['attributes']['feature_details']['title']
                logger.info(f"Processing {idx}/{total_count}: {title}")
                
                # Get download link
                download_info = scraper.download(item['attributes']['files'][0]['file_id'])
                
                # Download subtitle
                file_name = f"{title}_{args.language}.srt"
                if args.season is not None:
                    file_name = f"{title}_S{args.season:02d}"
                    if args.episode is not None:
                        file_name += f"E{args.episode:02d}"
                    file_name += f"_{args.language}.srt"
                
                downloader.download_subtitle(
                    download_url=download_info['link'],
                    title=title,
                    language=args.language,
                    file_name=file_name
                )
                success_count += 1
                
            except Exception as e:
                logger.error(f"Error downloading subtitle: {e}")
                continue
        
        # Report results
        logger.info(f"Download complete. Successfully downloaded {success_count}/{total_count} subtitles")
        return 0 if success_count > 0 else 1
                
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 