import asyncio
from app.config.celery_worker import celery_app
from app.config.consumer import kafka_avro_consumer


@celery_app.task
def consume_sales_task():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # If no loop exists, create one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(
        kafka_avro_consumer.poll_kafka_sales_created("sales_created")
    )
    print("✅ consume sales task completed")

