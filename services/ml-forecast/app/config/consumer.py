import struct
import json
import time
from io import BytesIO
from aiokafka import AIOKafkaConsumer
from fastavro import parse_schema, schemaless_reader
from app.config.schema_registry import SchemaRegistryClient
from app.config.settings import settings
from app.exceptions.types import (
    AvroDecodeError,
    KafkaConnectionError,
)

class KafkaAvroConsumer:
    def __init__(self):
        self.consumer: AIOKafkaConsumer | None = None
        self.schema_client = SchemaRegistryClient(settings.SCHEMA_REGISTRY_URL)
        self.schema_cache: dict[int, dict] = {}

    async def poll_kafka_sales_created(
        self,
        topic: str,
        max_second: int = 10,
        max_messages: int = 50,
    ):
        try:
            self.consumer = AIOKafkaConsumer(
                topic,
                bootstrap_servers=settings.KAFKA_BROKER,
                group_id=settings.ML_FORECAST_KAFKA_GROUP_ID,
                enable_auto_commit=False,
                auto_offset_reset="latest",
            )
            await self.consumer.start()
        except Exception as exc:
            raise KafkaConnectionError("Unable to start Kafka consumer") from exc

        start_time = time.time()
        messages_processed = 0

        try:
            async for msg in self.consumer:
                try:
                    value = await self.decode_avro(msg.value, topic)
                except AvroDecodeError as exc:
                    await self.consumer.commit()
                    continue


                # TODO: save to DB (levanta tu DatabaseError si algo falla)

                await self.consumer.commit()
                messages_processed += 1

                if (
                    time.time() - start_time > max_second
                    or messages_processed >= max_messages
                ):
                    break

        finally:
            await self.consumer.stop()

        return f"Processed {messages_processed} messages in {time.time() - start_time:.2f}s"

    # ------------------------------------------------------------------ #
    async def decode_avro(self, value: bytes, topic: str):
        # Avro Confluent wire format: magic byte (0) + 4‑byte schema id + payload
        try:
            magic, schema_id = struct.unpack(">bI", value[:5])
        except struct.error:
            raise AvroDecodeError("Invalid Avro header")

        if magic != 0:
            raise AvroDecodeError("Unknown magic byte")

        try:
            parsed_schema = self.schema_cache[schema_id]
        except KeyError:
            try:
                schema_json = await self.schema_client.get_schema(schema_id)
            except Exception as exc:
                raise AvroDecodeError(f"Schema id {schema_id} not found") from exc
            parsed_schema = parse_schema(json.loads(schema_json))
            self.schema_cache[schema_id] = parsed_schema

        bytes_reader = BytesIO(value[5:])
        try:
            return schemaless_reader(bytes_reader, parsed_schema)
        except Exception as exc:
            raise AvroDecodeError("Error decoding Avro payload") from exc


kafka_avro_consumer = KafkaAvroConsumer()
