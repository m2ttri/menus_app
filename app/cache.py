import json
import uuid
from typing import Any

import aioredis
from aioredis import RedisError


class Cache:
    def __init__(self):
        # Создание подключения к Redis
        self.rd = aioredis.Redis(host='redis', port=6379, db=0)

    async def check_connection(self):
        """Проверка подключения к Redis"""
        try:
            if await self.rd.ping():
                return True
        except RedisError:
            raise Exception('Failed to connect to Redis')
        return False

    async def get(self, key: str, parent_id: str | None = None, prefix: str = '') -> Any | None:
        """Возвращает значение если оно есть в кэше, если нет то возвращается None"""

        if parent_id:
            key = f'{parent_id}:{key}'  # noqa: E231
        if prefix:
            key = f'{prefix}:{key}'  # noqa: E231

        cache_value: str | None = await self.rd.get(str(key))
        if cache_value:
            return json.loads(cache_value)

        return None

    async def set(self, key: str, value: Any, parent_id: str | None = None, prefix: str = '', ex: int = 60) -> None:
        """Установка значения в кэш"""

        if parent_id:
            key = f'{parent_id}:{key}'  # noqa: E231
        if prefix:
            key = f'{prefix}:{key}'  # noqa: E231

        if isinstance(value, dict):
            for k in value:
                if isinstance(value[k], uuid.UUID):
                    value[k] = str(value[k])
            await self.rd.set(str(key), json.dumps(value), ex=ex)

    async def invalidate(self, key: str, parent_id: str | None = None, prefix: str = '') -> None:
        """Удаление значения из кэша"""

        if parent_id:
            key = f'{parent_id}:{key}'  # noqa: E231
        if prefix:
            key = f'{prefix}:{key}'  # noqa: E231

        await self.rd.delete(str(key))


cache: Cache = Cache()
