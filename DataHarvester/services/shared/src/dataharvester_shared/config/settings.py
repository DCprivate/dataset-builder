# Software/DataHarvester/services/shared/src/dataharvester_shared/config/settings.py

from functools import lru_cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig(BaseSettings):
    """MongoDB database settings."""
    host: str = "mongo"
    port: str = "27017"
    name: str = "dataharvester"
    user: str = "admin"
    password: str = "admin"

    @property
    def mongo_uri(self) -> str:
        """Generate MongoDB connection URI"""
        return f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

class Settings(BaseSettings):
    """Main settings for the application."""
    app_name: str = "DataHarvester"
    database: DatabaseConfig = DatabaseConfig()

@lru_cache
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()
