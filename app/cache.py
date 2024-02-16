import asyncio
import json
import uuid
from typing import Any

import aioredis
from aioredis import RedisError


class Cache:
    def __init__(self):
        self.rd = aioredis.Redis(host='redis', port=6379, db=0)
        self.lock = asyncio.Lock()
        self.dirty_flag = {}

    async def check_connection(self):
        """Проверка подключения к Redis"""
        try:
            if await self.rd.ping():
                return True
        except RedisError:
            raise Exception('Failed to connect to Redis')
        return False

    async def get(
            self,
            key: str,
            parent_id: str | None = None,
            prefix: str = ''
    ) -> Any | None:
        """Возврат данных из кэша"""

        async with self.lock:
            if parent_id:
                key = f'{parent_id}:{key}'  # noqa: E231
            if prefix:
                key = f'{prefix}:{key}'  # noqa: E231
            if self.dirty_flag.get(key):
                return None

            cache_value: str | None = await self.rd.get(str(key))

            if cache_value:
                return json.loads(cache_value)

        return None

    async def set(
            self,
            key: str,
            value: Any,
            parent_id: str | None = None,
            prefix: str = '',
            ex: int = 60
    ) -> None:
        """Установка значения в кэш"""

        async with self.lock:
            if parent_id:
                key = f'{parent_id}:{key}'  # noqa: E231
            if prefix:
                key = f'{prefix}:{key}'  # noqa: E231

            if isinstance(value, dict):
                for k in value:
                    if isinstance(value[k], uuid.UUID):
                        value[k] = str(value[k])
                await self.rd.set(
                    str(key),
                    json.dumps(value),
                    ex=ex
                )
        self.dirty_flag[key] = True

    async def invalidate(
            self,
            key: str,
            parent_id: str | None = None,
            prefix: str = ''
    ) -> None:
        """Удаление значения из кэша"""

        async with self.lock:
            if parent_id:
                key = f'{parent_id}:{key}'  # noqa: E231
            if prefix:
                key = f'{prefix}:{key}'  # noqa: E231

            await self.rd.delete(str(key))

            if key in self.dirty_flag:
                del self.dirty_flag[key]


cache: Cache = Cache()
