# Software/DataHarvester/services/data_ingestion/infrastructure/logging/logger.py

import logging
from datetime import datetime
from pathlib import Path

class LoggerSetup:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, 'initialized'):
            return
            
        self.initialized = True
        self.log_dir = Path('logs')
        self.log_dir.mkdir(exist_ok=True)
        
        # Create log filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = self.log_dir / f'youtube_scraper_{timestamp}.log'
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()  # Keep console output
            ]
        )
        
        # Suppress noisy loggers
        logging.getLogger('presidio-analyzer').setLevel(logging.ERROR)
        logging.getLogger('presidio').setLevel(logging.ERROR)
        
        # Create logger instance
        self.logger = logging.getLogger('youtube_scraper')
        self.logger.info(f'Logging initialized. Log file: {log_file}')

def get_logger():
    """Get the configured logger instance."""
    LoggerSetup()
    return logging.getLogger('youtube_scraper') 