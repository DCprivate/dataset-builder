# Software/DataHarvester/services/scraper_service/tests/integration/test_redis_integration.py

# pytest tests/integration/test_redis_integration.py -v

import pytest
import redis
import json
from datetime import datetime
from infrastructure.redis.producer import ScraperProducer
from infrastructure.redis.config import RedisSettings

@pytest.fixture(scope="session")
def redis_client():
    settings = RedisSettings()
    client = redis.Redis(
        host=settings.REDIS_HOST,  # This will now be "localhost"
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        decode_responses=True
    )
    # Test connection
    try:
        client.ping()
    except redis.ConnectionError:
        pytest.skip("Redis server is not available")
    
    yield client
    
    # Cleanup
    client.delete(settings.RAW_DATA_QUEUE)
    client.close()

@pytest.fixture
def producer():
    producer = ScraperProducer()
    yield producer
    producer.close()

class TestRedisIntegration:
    TEST_VIDEO_URL = "https://www.youtube.com/watch?v=4HLrtsGfusw"

    def test_end_to_end_queue(self, producer, redis_client):
        """Test complete queue operation"""
        content = "test content"
        metadata = {
            "video_url": self.TEST_VIDEO_URL,
            "language": "en"
        }
        
        success = producer.send_to_queue(content, metadata)
        assert success is True
        
        queued_data = redis_client.rpop(RedisSettings().RAW_DATA_QUEUE)
        assert queued_data is not None
        
        event = json.loads(queued_data)
        assert event["payload"]["content"] == content
        assert event["payload"]["metadata"] == metadata
        assert isinstance(datetime.fromisoformat(event["timestamp"]), datetime)

    @pytest.mark.integration
    def test_queue_persistence(self, producer, redis_client):
        """Test that data persists in queue"""
        producer.send_to_queue("test1", {"seq": 1})
        producer.send_to_queue("test2", {"seq": 2})
        
        assert redis_client.llen(RedisSettings().RAW_DATA_QUEUE) == 2

    @pytest.mark.integration
    def test_queue_order(self, producer, redis_client):
        """Test FIFO queue behavior"""
        producer.send_to_queue("first", {"seq": 1})
        producer.send_to_queue("second", {"seq": 2})
        
        first = json.loads(redis_client.rpop(RedisSettings().RAW_DATA_QUEUE))
        second = json.loads(redis_client.rpop(RedisSettings().RAW_DATA_QUEUE))
        
        assert first["payload"]["metadata"]["seq"] == 1
        assert second["payload"]["metadata"]["seq"] == 2