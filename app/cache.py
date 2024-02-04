import json
import uuid
from typing import Any

import aioredis


class Cache:
    def __init__(self):
        # Создание подключения к Redis
        self.rd = aioredis.Redis(host='redis', port=6379, db=0)

    async def get(self, key: str) -> Any | None:
        """Возвращает значение если оно есть в кэше, если нет то возвращается None"""
        cache_value: str | None = await self.rd.get(str(key))
        if cache_value:
            return json.loads(cache_value)
        return None

    async def set(self, key: str, value: Any, ex: int = 60) -> None:
        """Установка значения в кэш"""

        # Если значение является словарем
        if isinstance(value, dict):
            # проходим по всем ключам в словаре:
            for k in value:
                # если значение ключа является UUID
                if isinstance(value[k], uuid.UUID):
                    # то преобразуем его в строку
                    value[k] = str(value[k])
            # Устанавливаем значение в Redis
            await self.rd.set(str(key), json.dumps(value), ex=ex)

    async def invalidate(self, key: str) -> None:
        """Удаление значения из кэша по ключу"""
        await self.rd.delete(str(key))


cache: Cache = Cache()
