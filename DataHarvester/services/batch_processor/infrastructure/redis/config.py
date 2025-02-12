# Software/DataHarvester/services/batch_processor/infrastructure/redis/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='REDIS_')
    
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PREFIX: str = "scraper"
    RAW_DATA_QUEUE: str = "raw_data_queue"
    REDIS_PASSWORD: str | None = None
    
    # Queue names
    PROCESSING_QUEUE: str = "processing_queue"
    
    # Batch processing settings
    BATCH_SIZE: int = 100
    PROCESSING_TIMEOUT: int = 30
    
    class Config:
        env_prefix = "REDIS_" 