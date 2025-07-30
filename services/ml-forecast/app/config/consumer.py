import struct
import json
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

    async def start(self, topic: str):
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id=settings.KAFKA_GROUP_ID,
            enable_auto_commit=True,
            auto_offset_reset="earliest"
        )
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                decoded = await self.decode_avro(msg.value, msg.topic)
                print(f"Message from: {msg.topic}: {decoded}")
        finally:
            await self.consumer.stop()

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
