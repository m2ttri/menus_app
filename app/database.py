from typing import AsyncGenerator

from sqlalchemy import MetaData, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

metadata = MetaData()

engine = create_async_engine(settings.DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


# Асинхронная функция, возвращающая сессию SQLAlchemy
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        # Проверка подключения к бд
        try:
            await session.execute(text('SELECT 1'))
        except OperationalError:
            raise Exception('Failed to connect to database')
        else:
            yield session
