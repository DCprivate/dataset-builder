# Software/DataHarvester/services/scraper_service/tests/infrastructure/redis/test_producer.py

# pytest tests/infrastructure/redis/test_producer.py -v

import pytest
from datetime import datetime, timezone
from infrastructure.redis.producer import ScraperProducer

@pytest.fixture
def mock_redis(mocker):
    mock = mocker.patch('redis.Redis')
    mock.return_value.lpush.return_value = 1
    return mock

@pytest.fixture
def producer(mock_redis):
    return ScraperProducer()

class TestScraperProducer:
    TEST_VIDEO_URL = "https://www.youtube.com/watch?v=4HLrtsGfusw"
    
    def test_create_event_structure(self, producer):
        """Test event creation and structure"""
        content = "test content"
        metadata = {"url": self.TEST_VIDEO_URL}
        
        event = producer.create_event(content, metadata)
        
        assert isinstance(event["event_id"], str)
        assert event["event_type"] == "raw_data"
        assert event["payload"]["content"] == content
        assert event["payload"]["metadata"] == metadata
        assert isinstance(datetime.fromisoformat(event["timestamp"]), datetime)
        assert event["service"] == "scraper_service"

    def test_send_to_queue_success(self, producer, mock_redis):
        """Test successful queue operation"""
        result = producer.send_to_queue("test content", {"test": "metadata"})
        assert result is True
        mock_redis.return_value.lpush.assert_called_once()

    def test_send_to_queue_failure(self, producer, mocker):
        """Test queue operation failure handling"""
        mocker.patch.object(producer.redis_client, 'lpush', side_effect=Exception("Redis error"))
        result = producer.send_to_queue("test content", {"test": "metadata"})
        assert result is False

    def test_event_timestamp_timezone(self, producer):
        """Test that event timestamps are timezone-aware UTC"""
        event = producer.create_event("test", {})
        timestamp = datetime.fromisoformat(event["timestamp"])
        assert timestamp.tzinfo is not None
        assert timestamp.tzinfo == timezone.utc

    def test_create_event(self, producer):
        """Test event creation format"""
        content = "test content"
        metadata = {"url": self.TEST_VIDEO_URL}
        
        event = producer.create_event(content, metadata)
        
        assert "event_id" in event
        assert event["event_type"] == "raw_data"
        assert event["payload"]["content"] == content
        assert event["payload"]["metadata"] == metadata
        assert "timestamp" in event
        assert event["service"] == "scraper_service" 