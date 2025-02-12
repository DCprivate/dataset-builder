# DataHarvester/services/batch_processor/infrastructure/redis/consumer.py

import json
import logging
from typing import List, Dict, Any
import aioredis
from .config import RedisSettings

logger = logging.getLogger(__name__)

class BatchConsumer:
    def __init__(self):
        self.settings = RedisSettings()
        self.redis_client = aioredis.Redis(
            host=self.settings.REDIS_HOST,
            port=self.settings.REDIS_PORT,
            db=self.settings.REDIS_DB,
            password=self.settings.REDIS_PASSWORD,
            decode_responses=True
        )
    
    async def get_batch(self) -> List[Dict[str, Any]]:
        """Fetch a batch of messages from the raw data queue"""
        try:
            batch = []
            for _ in range(self.settings.BATCH_SIZE):
                result = await self.redis_client.brpop(
                    self.settings.RAW_DATA_QUEUE,
                    timeout=self.settings.PROCESSING_TIMEOUT
                )
                
                if not result:
                    break
                    
                _, message = result
                batch.append(json.loads(message))
            
            logger.info(f"Retrieved batch of {len(batch)} messages")
            return batch
            
        except Exception as e:
            logger.error(f"Error fetching batch: {str(e)}")
            return []
    
    def close(self):
        """Close Redis connection"""
        self.redis_client.close()