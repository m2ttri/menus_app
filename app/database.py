from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

# Создание объекта метаданных для работы с базой данных
metadata = MetaData()

# Создание асинхронного движка SQLAlchemy для подключения к базе данных
engine = create_async_engine(settings.DATABASE_URL)

# Создание асинхронной фабрики сессий SQLAlchemy
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Базовый класс для моделей SQLAlchemy
class Base(DeclarativeBase):
    pass


# Асинхронная функция, возвращающая сессию SQLAlchemy
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
