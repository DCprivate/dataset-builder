# /services/data_transformation/interfaces/api/dependencies.py

import logging
from typing import AsyncIterator
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dataharvester_shared.config.settings import get_settings

settings = get_settings()

async def get_db() -> AsyncIterator[AsyncIOMotorDatabase]:
    """Database Connection Dependency."""
    client = AsyncIOMotorClient(settings.database.mongo_uri)
    try:
        yield client[settings.database.name]
    except Exception as ex:
        logging.error(f"Database connection error: {ex}")
        raise
    finally:
        client.close()