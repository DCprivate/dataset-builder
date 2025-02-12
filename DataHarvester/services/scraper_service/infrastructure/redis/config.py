# Software/DataHarvester/services/scraper_service/infrastructure/redis/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='REDIS_')
    
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PREFIX: str = "scraper"
    
    # Queue names
    RAW_DATA_QUEUE: str = "raw_data_queue"
    
    # Optional authentication
    REDIS_PASSWORD: str | None = None