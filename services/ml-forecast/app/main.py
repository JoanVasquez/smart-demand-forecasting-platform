import uvicorn
import asyncio
from fastapi import FastAPI
from dotenv import load_dotenv
from app.config.consumer import KafkaAvroConsumer
from app.forecast.router.routes import router as v1_router
from aiokafka.errors import KafkaConnectionError

load_dotenv()


async def start_consumer_with_retry(consumer, topic, retries=10, delay=5):
    for attempt in range(retries):
        try:
            await consumer.start(topic)
            break
        except KafkaConnectionError:
            print(f"[Retry {attempt+1}/{retries}] Kafka not ready, retrying in {delay}s...")
            await asyncio.sleep(delay)


def create_app() -> FastAPI:
    app = FastAPI(title="ML Forecast Service", version="1.0.0")
    app.include_router(v1_router, prefix="/api/v1")

    consumer = KafkaAvroConsumer()
    asyncio.create_task(start_consumer_with_retry(consumer, "sales_created"))

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True
    )
