import asyncio
from app.config.celery_worker import celery_app
from app.config.consumer import kafka_avro_consumer


@celery_app.task
def consume_sales_task():
    result = asyncio.run(kafka_avro_consumer.poll_kafka_sales_created("sales_created"))
    print(f"consume sales task completed")

