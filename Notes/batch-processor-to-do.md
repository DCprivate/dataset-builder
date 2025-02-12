Here's a detailed summary of what we've implemented so far in the event-driven batch processor architecture:

### Completed Implementations:

1. **Scraper Service Redis Integration**
- Implemented Redis producer for sending scraped data
- Added Redis configuration management
- Created standardized event message format
- Completed unit tests for the producer
- Integration tests are written but pending Redis server

2. **Batch Processor Initial Setup**
- Implemented Redis configuration management
- Created BatchConsumer for fetching data from raw_data_queue
- Created BatchProducer for sending to processing_queue
- Defined batch processing settings (size, timeout)

### Current State of Files:

1. **Scraper Service**
````
services/scraper_service/
├── infrastructure/redis/
│   ├── config.py         ✓ Complete
│   └── producer.py       ✓ Complete
└── tests/
    ├── infrastructure/redis/
    │   └── test_producer.py  ✓ Complete
    └── integration/
        └── test_redis_integration.py  ✓ Complete
````

2. **Batch Processor**
````
services/batch_processor/
└── infrastructure/redis/
    ├── config.py         ✓ Complete
    ├── consumer.py       ✓ Complete
    └── producer.py       ✓ Complete
````

### Next Steps:

1. **Batch Processor Celery Implementation**
- Implement celery_config.py
- Implement tasks.py with batch processing logic
- Add Celery beat scheduling

2. **Testing Infrastructure**
- Write unit tests for BatchConsumer
- Write unit tests for BatchProducer
- Write integration tests for batch processing
- Write Celery task tests

3. **Transformer Service Integration**
- Implement Redis consumer for processing_queue
- Add transformer service producer
- Connect to LLM processing pipeline

### Current Data Flow:
````
[Scraper Service]
      ↓
      ↓ (raw_data_queue)
      ↓
[Batch Processor] (in progress)
      ↓
      ↓ (processing_queue)
      ↓
[Transformer Service] (not started)
````

### Environment Requirements:
- Redis server
- Python 3.12.8
- Celery
- pytest for testing

Would you like me to provide any specific implementation details for the next steps when you return?



# step 2 has yet to be implemented

Great! Now let's implement the batch processor service. This service will act as a bridge between the scraper and transformer services, handling the queue consumption and task distribution.

### Step 1: Redis Consumer/Producer Setup

First, let's implement the Redis consumer and producer for the batch processor:

````python:DataHarvester/services/batch_processor/infrastructure/redis/config.py
# infrastructure/redis/config.py

from pydantic_settings import BaseSettings

class RedisSettings(BaseSettings):
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None
    
    # Queue names
    RAW_DATA_QUEUE: str = "raw_data_queue"
    PROCESSING_QUEUE: str = "processing_queue"
    
    # Batch settings
    BATCH_SIZE: int = 10
    PROCESSING_TIMEOUT: int = 300  # seconds
    
    class Config:
        env_prefix = "REDIS_"
````

````python:DataHarvester/services/batch_processor/infrastructure/redis/consumer.py
# infrastructure/redis/consumer.py

import json
import logging
from typing import List, Dict, Any
import redis
from .config import RedisSettings

logger = logging.getLogger(__name__)

class BatchConsumer:
    def __init__(self):
        self.settings = RedisSettings()
        self.redis_client = redis.Redis(
            host=self.settings.REDIS_HOST,
            port=self.settings.REDIS_PORT,
            db=self.settings.REDIS_DB,
            password=self.settings.REDIS_PASSWORD,
            decode_responses=True
        )
    
    def get_batch(self) -> List[Dict[str, Any]]:
        """Fetch a batch of messages from the raw data queue"""
        try:
            batch = []
            for _ in range(self.settings.BATCH_SIZE):
                # Use BRPOP for blocking read with timeout
                result = self.redis_client.brpop(
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
````

````python:DataHarvester/services/batch_processor/infrastructure/redis/producer.py
# infrastructure/redis/producer.py

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
````

### Step 2: Update Celery Tasks

Now let's update the Celery configuration and tasks:

````python:DataHarvester/services/batch_processor/pipeline_worker/celery_config.py
# pipeline_worker/celery_config.py

from celery import Celery
from infrastructure.redis.config import RedisSettings

settings = RedisSettings()

celery_app = Celery(
    'batch_processor',
    broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}',
    backend=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}'
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

celery_app.autodiscover_tasks(['pipeline_worker.tasks'])
````

````python:DataHarvester/services/batch_processor/pipeline_worker/tasks.py
# pipeline_worker/tasks.py

import logging
from celery import Task
from .celery_config import celery_app
from infrastructure.redis.consumer import BatchConsumer
from infrastructure.redis.producer import BatchProducer

logger = logging.getLogger(__name__)

class BatchProcessingTask(Task):
    _consumer = None
    _producer = None
    
    @property
    def consumer(self) -> BatchConsumer:
        if self._consumer is None:
            self._consumer = BatchConsumer()
        return self._consumer
    
    @property
    def producer(self) -> BatchProducer:
        if self._producer is None:
            self._producer = BatchProducer()
        return self._producer

@celery_app.task(base=BatchProcessingTask, bind=True)
def process_batch(self) -> bool:
    """Process a batch of messages"""
    try:
        # Get batch from raw data queue
        batch = self.consumer.get_batch()
        
        if not batch:
            logger.info("No messages to process")
            return True
        
        # Send to processing queue
        success = self.producer.send_to_processing(batch)
        
        if not success:
            logger.error("Failed to send batch to processing queue")
            # Could implement retry logic here
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error processing batch: {str(e)}")
        return False
````

### Step 3: Add Celery Beat Schedule

Let's add a scheduled task to regularly process batches:

````python:DataHarvester/services/batch_processor/pipeline_worker/celery_config.py
# Add to celery_config.py

from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    'process-batch': {
        'task': 'pipeline_worker.tasks.process_batch',
        'schedule': crontab(minute='*/1'),  # Run every minute
    },
}
````

Would you like me to provide the test cases next? Or would you prefer to implement and test this part first?

The tests should cover:
1. Batch consumer functionality
2. Batch producer functionality
3. Celery task execution
4. Integration tests with Redis





Let's continue with implementing the Batch Processor. Here's the detailed next steps:

### 1. First, Let's Set Up Testing Infrastructure

Create these test files:

````python:DataHarvester/services/batch_processor/tests/infrastructure/redis/test_consumer.py
import pytest
import json
from unittest.mock import Mock, patch
from infrastructure.redis.consumer import BatchConsumer
from infrastructure.redis.config import RedisSettings

class TestBatchConsumer:
    @pytest.fixture
    def consumer(self):
        return BatchConsumer()
    
    @pytest.fixture
    def mock_redis_client(self):
        with patch('redis.Redis') as mock_redis:
            yield mock_redis.return_value
    
    def test_get_batch_empty_queue(self, consumer, mock_redis_client):
        mock_redis_client.brpop.return_value = None
        batch = consumer.get_batch()
        assert len(batch) == 0
    
    def test_get_batch_success(self, consumer, mock_redis_client):
        # Prepare test data
        test_messages = [
            {
                "event_id": "test1",
                "event_type": "raw_data",
                "payload": {"content": "test1"}
            },
            {
                "event_id": "test2",
                "event_type": "raw_data",
                "payload": {"content": "test2"}
            }
        ]
        
        # Mock Redis responses
        mock_redis_client.brpop.side_effect = [
            ("queue", json.dumps(msg)) for msg in test_messages
        ] + [None]  # Add None to simulate empty queue
        
        batch = consumer.get_batch()
        assert len(batch) == 2
        assert batch[0]["event_id"] == "test1"
        assert batch[1]["event_id"] == "test2"
    
    def test_get_batch_redis_error(self, consumer, mock_redis_client):
        mock_redis_client.brpop.side_effect = Exception("Redis error")
        batch = consumer.get_batch()
        assert len(batch) == 0
````


````python:DataHarvester/services/batch_processor/tests/infrastructure/redis/test_producer.py
import pytest
import json
from unittest.mock import Mock, patch
from infrastructure.redis.producer import BatchProducer

class TestBatchProducer:
    @pytest.fixture
    def producer(self):
        return BatchProducer()
    
    @pytest.fixture
    def mock_redis_client(self):
        with patch('redis.Redis') as mock_redis:
            yield mock_redis.return_value
    
    def test_create_batch_event(self, producer):
        test_batch = [
            {"event_id": "1", "payload": {"content": "test1"}},
            {"event_id": "2", "payload": {"content": "test2"}}
        ]
        
        event = producer.create_batch_event(test_batch)
        assert event["event_type"] == "batch_processing"
        assert event["payload"]["size"] == 2
        assert "timestamp" in event
        assert "event_id" in event
    
    def test_send_to_processing_empty_batch(self, producer):
        result = producer.send_to_processing([])
        assert result is False
    
    def test_send_to_processing_success(self, producer, mock_redis_client):
        test_batch = [
            {"event_id": "1", "payload": {"content": "test1"}},
            {"event_id": "2", "payload": {"content": "test2"}}
        ]
        
        result = producer.send_to_processing(test_batch)
        assert result is True
        mock_redis_client.lpush.assert_called_once()
    
    def test_send_to_processing_redis_error(self, producer, mock_redis_client):
        mock_redis_client.lpush.side_effect = Exception("Redis error")
        test_batch = [{"event_id": "1", "payload": {"content": "test"}}]
        
        result = producer.send_to_processing(test_batch)
        assert result is False
````


````python:DataHarvester/services/batch_processor/tests/integration/test_redis_integration.py
import pytest
import json
import redis
from infrastructure.redis.consumer import BatchConsumer
from infrastructure.redis.producer import BatchProducer
from infrastructure.redis.config import RedisSettings

@pytest.mark.integration
class TestRedisIntegration:
    @pytest.fixture(scope="class")
    def redis_client(self):
        settings = RedisSettings()
        client = redis.Redis(
            host=settings.REDIS_HOST,
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
        client.flushdb()
        client.close()
    
    @pytest.fixture
    def consumer(self):
        return BatchConsumer()
    
    @pytest.fixture
    def producer(self):
        return BatchProducer()
    
    def test_batch_processing_flow(self, redis_client, consumer, producer):
        # Create test batch
        test_batch = [
            {"event_id": "1", "payload": {"content": "test1"}},
            {"event_id": "2", "payload": {"content": "test2"}}
        ]
        
        # Send batch to processing queue
        assert producer.send_to_processing(test_batch) is True
        
        # Verify message in queue
        result = redis_client.llen(RedisSettings().PROCESSING_QUEUE)
        assert result == 1
        
        # Read and verify message
        message = redis_client.rpop(RedisSettings().PROCESSING_QUEUE)
        assert message is not None
        
        data = json.loads(message)
        assert data["event_type"] == "batch_processing"
        assert len(data["payload"]["batch"]) == 2
    
    def test_batch_size_limit(self, redis_client, consumer, producer):
        settings = RedisSettings()
        
        # Create more messages than batch size
        test_messages = [
            {"event_id": str(i), "payload": {"content": f"test{i}"}}
            for i in range(settings.BATCH_SIZE + 5)
        ]
        
        # Send all messages to raw data queue
        for msg in test_messages:
            redis_client.lpush(settings.RAW_DATA_QUEUE, json.dumps(msg))
        
        # Get batch and verify size
        batch = consumer.get_batch()
        assert len(batch) <= settings.BATCH_SIZE
````


### 2. Update Celery Task Implementation

````python:DataHarvester/services/batch_processor/tests/pipeline_worker/test_tasks.py
import pytest
from unittest.mock import Mock, patch
from pipeline_worker.tasks import process_batch
from infrastructure.redis.consumer import BatchConsumer
from infrastructure.redis.producer import BatchProducer

class TestBatchProcessingTask:
    @pytest.fixture
    def mock_consumer(self):
        with patch('infrastructure.redis.consumer.BatchConsumer') as mock:
            consumer = Mock(spec=BatchConsumer)
            mock.return_value = consumer
            yield consumer
    
    @pytest.fixture
    def mock_producer(self):
        with patch('infrastructure.redis.producer.BatchProducer') as mock:
            producer = Mock(spec=BatchProducer)
            mock.return_value = producer
            yield producer
    
    def test_process_batch_empty(self, mock_consumer, mock_producer):
        mock_consumer.get_batch.return_value = []
        
        result = process_batch.apply().get()
        assert result is True
        mock_producer.send_to_processing.assert_not_called()
    
    def test_process_batch_success(self, mock_consumer, mock_producer):
        test_batch = [
            {"event_id": "1", "payload": {"content": "test1"}},
            {"event_id": "2", "payload": {"content": "test2"}}
        ]
        mock_consumer.get_batch.return_value = test_batch
        mock_producer.send_to_processing.return_value = True
        
        result = process_batch.apply().get()
        assert result is True
        mock_producer.send_to_processing.assert_called_once_with(test_batch)
    
    def test_process_batch_producer_failure(self, mock_consumer, mock_producer):
        test_batch = [{"event_id": "1", "payload": {"content": "test"}}]
        mock_consumer.get_batch.return_value = test_batch
        mock_producer.send_to_processing.return_value = False
        
        result = process_batch.apply().get()
        assert result is False
````


### 3. Add Configuration for pytest

````toml:DataHarvester/services/batch_processor/pyproject.toml
[tool.pytest]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --tb=short"
markers = [
    "integration: marks tests as integration tests"
]
````


### Next Steps After Testing:

1. Implement Celery worker startup script
2. Add Docker configuration for the batch processor
3. Begin transformer service implementation

Would you like me to provide any of these next steps or would you like to implement and test the current changes first?


