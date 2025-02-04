# Software/DataHarvester/services/worker/pipeline_worker/celery_config.py

from celery import Celery
from dataharvester_shared.config.settings import get_settings

settings = get_settings()

def create_celery_app():
    app = Celery('tasks')
    app.conf.update(
        broker_url=f"redis://{settings.app_name}_redis:6379/0",
        result_backend=f"redis://{settings.app_name}_redis:6379/0",
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        enable_utc=True,
        broker_connection_retry_on_startup=True,
    )
    return app

celery_app = create_celery_app()

# Update the autodiscover_tasks to look in the correct location
celery_app.autodiscover_tasks(['pipeline_worker.tasks'])

if __name__ == '__main__':
    celery_app.start() 