from celery import Celery
from celery.schedules import crontab
from app.config.settings import settings

celery_app = Celery("worker")

celery_app.conf.update(
    broker_url=settings.REDIS_HOST,
    result_backend=settings.REDIS_HOST,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True
)

celery_app.conf.beat_schedule = {
    "consume-kafka-every-30s": {
        "task": "app.config.tasks.consume_sales_task",
        "schedule": 30.0
    }
}

celery_app.autodiscover_tasks(["app.config"])
