import struct
import json
import time
from aiokafka import AIOKafkaConsumer
from fastavro import parse_schema, schemaless_reader
from io import IOBase, BytesIO
from app.config.schema_registry import SchemaRegistryClient
from app.config.settings import settings

class KafkaAvroConsumer:
    def __init__(self):
        self.consumer = None
        self.schema_client = SchemaRegistryClient(settings.SCHEMA_REGISTRY_URL)
        self.schema_cache = {}

    async def poll_kafka_sales_created(self, topic: str, max_second: int = 10, max_messages: int = 50):
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id=settings.KAFKA_GROUP_ID,
            enable_auto_commit=False,
            auto_offset_reset="latest"
        )
        await self.consumer.start()
        start_time = time.time()
        messages_processed = 0

        try:
            async for msg in self.consumer:
                value = await self.decode_avro(msg.value, topic)
                # save to the DB here: TODO

                await self.consumer.commit()
                messages_processed += 1

                if (time.time() - start_time > max_second) or (messages_processed >= max_messages):
                    await self.consumer.stop()
                    return f"Processed {messages_processed} messages"

        finally:
            await self.consumer.stop()

        return f"Processed {messages_processed} messages in {time.time() - start_time:.2f}s"

    async def decode_avro(self, value: bytes, topic: str):
        magic, schema_id = struct.unpack(">bI", value[:5])
        if magic != 0:
            raise ValueError("Unknown magic byte")

        schema_json = await self.schema_client.get_schema(schema_id)
        parsed_schema = self.schema_cache.get(schema_id)

        if not parsed_schema:
            parsed_schema = parse_schema(json.loads(schema_json))
            self.schema_cache[schema_id] = parsed_schema

        bytes_reader = BytesIO(value[5:])
        return schemaless_reader(bytes_reader, parsed_schema)

kafka_avro_consumer = KafkaAvroConsumer()
