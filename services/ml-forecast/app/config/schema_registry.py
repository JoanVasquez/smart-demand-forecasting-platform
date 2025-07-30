import httpx

class SchemaRegistryClient:
    def __init__(self, registry_url: str):
        self.registry_url = registry_url.rstrip("/")
        self.cache = {}

    async def get_schema(self, schema_id: int):
        if schema_id in self.cache:
            return self.cache[schema_id]

        url = f"{self.registry_url}/schemas/ids/{schema_id}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            resp.raise_for_status()
            schema = resp.json()["schema"]
            self.cache[schema_id] = schema
            return schema

