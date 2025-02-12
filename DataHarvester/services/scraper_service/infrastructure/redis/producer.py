# Software/DataHarvester/services/scraper_service/infrastructure/redis/producer.py

import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any
from uuid import uuid4

import redis
from .config import RedisSettings

logger = logging.getLogger(__name__)

class ScraperProducer:
    def __init__(self):
        self.settings = RedisSettings()
        self.redis_client = redis.Redis(
            host=self.settings.REDIS_HOST,
            port=self.settings.REDIS_PORT,
            db=self.settings.REDIS_DB,
            password=self.settings.REDIS_PASSWORD,
            decode_responses=True
        )
        
    def create_event(self, content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create a standardized event message"""
        return {
            "event_id": str(uuid4()),
            "event_type": "raw_data",
            "payload": {
                "content": content,
                "metadata": metadata
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": "scraper_service"
        }
    
    def send_to_queue(self, content: str, metadata: Dict[str, Any]) -> bool:
        """Send scraped data to Redis queue"""
        try:
            event = self.create_event(content, metadata)
            self.redis_client.lpush(
                self.settings.RAW_DATA_QUEUE,
                json.dumps(event)
            )
            logger.info(f"Successfully queued event {event['event_id']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to queue event: {str(e)}")
            return False
            
    def close(self):
        """Close Redis connection"""
        self.redis_client.close()