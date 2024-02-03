import json
import uuid

import aioredis


class Cache:
    def __init__(self):
        self.rd = aioredis.Redis(host='redis', port=6379, db=0)

    async def get(self, key):
        cache = await self.rd.get(str(key))
        if cache:
            return json.loads(cache)
        return None

    async def set(self, key, value, ex=60):
        if isinstance(value, dict):
            for k in value:
                if isinstance(value[k], uuid.UUID):
                    value[k] = str(value[k])
            await self.rd.set(str(key), json.dumps(value), ex=ex)

    async def invalidate(self, key):
        await self.rd.delete(str(key))


cache = Cache()
