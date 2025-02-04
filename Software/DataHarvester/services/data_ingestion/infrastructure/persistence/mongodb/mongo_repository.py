# Software/DataHarvester/src/infrastructure/database/mongo_client.py

from infrastructure.logging.logger import get_logger
from functools import wraps
import time
from typing import Optional, Dict, Any, List
from infrastructure.config.config_manager import ConfigManager
from infrastructure.error_handling.middleware.error_middleware import ErrorMiddleware
from domain.exceptions.domain_exceptions import DatabaseError
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import errors as pymongo_errors

logger = get_logger()
config = ConfigManager().get_config('database')

def retry_connection(retries=None, delay=None):
    """Decorator for retrying database operations."""
    if retries is None:
        retries = config['retry']['max_attempts']
    if delay is None:
        delay = config['retry']['initial_delay']
        
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(retries):
                try:
                    return await func(*args, **kwargs)
                except pymongo_errors.PyMongoError as e:
                    last_error = e
                    if attempt < retries - 1:
                        logger.warning(f"Database operation failed, attempt {attempt + 1}/{retries}: {str(e)}")
                        # Exponential backoff
                        time.sleep(delay * (config['retry']['exponential_base'] ** attempt))
                    else:
                        logger.error(f"Database operation failed after {retries} attempts: {str(e)}")
                        raise
            if last_error:  # Only raise if there's an actual error
                raise last_error
            raise Exception("Unknown error occurred")  # Fallback
        return wrapper
    return decorator

class MongoDBClient:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Sync init for basic setup"""
        self._initialized = False

    @classmethod
    async def create(cls, mongo_uri: str | None = None, database: str | None = None):
        """Async factory method for initialization"""
        self = cls()
        if not self._initialized:
            await self.initialize(mongo_uri, database)
            self._initialized = True
        return self

    async def initialize(self, mongo_uri: str | None = None, database: str | None = None):
        """Initialize MongoDB connection."""
        try:
            self.mongo_uri = mongo_uri or "mongodb://mongo:27017/"
            self.database_name = database or "youtube_transcripts"
            self.client = AsyncIOMotorClient(self.mongo_uri)
            self.db = self.client[self.database_name]
            await self.client.admin.command('ping')
            logger.info(f"Connected to MongoDB at {self.mongo_uri}")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise
    
    async def store_video(self, video_id: str, transcripts: list) -> bool:
        """Store video transcripts in MongoDB."""
        try:
            collection = self.db.raw_transcripts
            result = await collection.update_one(
                {"video_id": video_id},
                {"$set": {
                    "video_id": video_id,
                    "transcripts": transcripts,
                    "processed": False
                }},
                upsert=True
            )
            logger.info(f"Stored/updated video {video_id} in MongoDB")
            return True
        except Exception as e:
            logger.error(f"Failed to store video {video_id}: {str(e)}")
            return False
    
    async def get_video(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve video transcripts from MongoDB."""
        try:
            collection = self.db.raw_transcripts
            return await collection.find_one({"video_id": video_id})
        except Exception as e:
            logger.error(f"Failed to retrieve video {video_id}: {str(e)}")
            return None
    
    async def mark_video_processed(self, video_id: str) -> bool:
        """Mark a video as processed."""
        try:
            collection = self.db.raw_transcripts
            result = await collection.update_one(
                {"video_id": video_id},
                {"$set": {"processed": True}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to mark video {video_id} as processed: {str(e)}")
            return False

    async def _setup_indexes(self):
        """Setup database indexes based on configuration."""
        try:
            for collection_name, settings in config['collections'].items():
                collection = self.db[collection_name]
                for index in settings['indexes']:
                    await collection.create_index(
                        index['fields'],
                        unique=index.get('unique', False)
                    )
        except Exception as e:
            logger.error(f"Failed to setup indexes: {str(e)}")
            raise

    @ErrorMiddleware.catch_errors(context="MongoDB")
    async def store_video_async(self, video_id: str, transcripts: List[Dict]) -> None:
        try:
            await self.db.transcripts.update_one(
                {"video_id": video_id},
                {"$set": {"transcripts": transcripts, "processed": False}},
                upsert=True
            )
            logger.info(f"Successfully inserted/updated transcripts for video {video_id}")
        except pymongo_errors.PyMongoError as e:
            raise DatabaseError(f"Failed to store video {video_id}", "DB003") from e

    @retry_connection(retries=3, delay=1)
    async def get_transcript(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve transcript document with retry mechanism."""
        try:
            result = await self.db.transcripts.find_one({"video_id": video_id})
            return result
        except pymongo_errors.PyMongoError as e:
            logger.error(f"Failed to retrieve transcripts for video {video_id}: {str(e)}")
            raise

    @retry_connection(retries=3, delay=1)
    async def update_processed_status(self, video_id: str, processed: bool = True) -> bool:
        """Update processing status with retry mechanism."""
        try:
            result = await self.db.transcripts.update_one(
                {"video_id": video_id},
                {"$set": {"processed": processed}}
            )
            return result.modified_count > 0
        except pymongo_errors.PyMongoError as e:
            logger.error(f"Failed to update processing status for video {video_id}: {str(e)}")
            raise

    async def cleanup(self) -> None:
        """Cleanup database connections."""
        try:
            if hasattr(self, 'client'):
                self.client.close()
                logger.info("MongoDB connection closed successfully")
        except Exception as e:
            logger.error(f"Error during database cleanup: {str(e)}")

    def __del__(self):
        """Ensure cleanup on object destruction."""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.cleanup())
            else:
                loop.run_until_complete(self.cleanup())
        except Exception as e:
            logger.error(f"Error during cleanup in __del__: {str(e)}")

    async def store_raw_transcripts(self, video_id: str, data: Dict[str, Any]) -> bool:
        """Store raw transcript data."""
        try:
            result = await self.db.raw_transcripts.update_one(
                {'video_id': video_id},
                {'$set': data},
                upsert=True
            )
            if result.acknowledged:
                logger.info(f"Stored raw transcripts for video {video_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to store raw transcripts for {video_id}: {str(e)}")
            raise

    async def store_processed_transcripts(self, video_id: str, data: Dict[str, Any]) -> bool:
        """Store processed transcript data."""
        try:
            result = await self.db.processed_transcripts.update_one(
                {'video_id': video_id},
                {'$set': data},
                upsert=True
            )
            if result.acknowledged:
                logger.info(f"Stored processed transcripts for video {video_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to store processed transcripts for {video_id}: {str(e)}")
            raise 