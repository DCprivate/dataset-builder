# Software/DataHarvester/services/batch_processor/infrastructure/redis/producer.py

import json
import logging
from typing import Dict, Any, List
from datetime import datetime
from uuid import uuid4
import redis
from .config import RedisSettings

logger = logging.getLogger(__name__)

class BatchProducer:
    def __init__(self):
        self.settings = RedisSettings()
        self.redis_client = redis.Redis(
            host=self.settings.REDIS_HOST,
            port=self.settings.REDIS_PORT,
            db=self.settings.REDIS_DB,
            password=self.settings.REDIS_PASSWORD,
            decode_responses=True
        )
    
    def create_batch_event(self, batch: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a batch event for processing"""
        return {
            "event_id": str(uuid4()),
            "event_type": "batch_processing",
            "payload": {
                "batch": batch,
                "size": len(batch)
            },
            "timestamp": datetime.utcnow().isoformat(),
            "service": "batch_processor"
        }
    
    def send_to_processing(self, batch: List[Dict[str, Any]]) -> bool:
        """Send batch to processing queue"""
        try:
            if not batch:
                logger.warning("Attempted to send empty batch")
                return False
                
            event = self.create_batch_event(batch)
            self.redis_client.lpush(
                self.settings.PROCESSING_QUEUE,
                json.dumps(event)
            )
            
            logger.info(f"Successfully queued batch event {event['event_id']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to queue batch: {str(e)}")
            return False
    
    def close(self):
        """Close Redis connection"""
        self.redis_client.close()