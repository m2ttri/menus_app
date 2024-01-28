import os
import pytest
import asyncio
import asyncpg
from httpx import AsyncClient
from typing import AsyncGenerator
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from app.database import get_async_session, Base
from app.config import settings
from app.main import app


load_dotenv()

host = os.getenv("DB_HOST_TEST")
user = os.getenv("DB_USER_TEST")
password = os.getenv("DB_PASS_TEST")
database = os.getenv("DB_NAME_TEST")


engine_test = create_async_engine(settings.TEST_DATABASE_URL, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    """Создание таблиц в тестовой бд и удаление после завершения работы тестов"""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


async def execute_query(query: str):
    """Выполнить SQL запрос и вернуть результат"""
    conn = await asyncpg.connect(host=host,
                                 user=user,
                                 password=password,
                                 database=database)
    result = await conn.fetchrow(query)
    await conn.close()
    return result


async def get_menu_instance():
    """Получить меню"""
    return await execute_query('SELECT * FROM menus LIMIT 1')


async def get_submenu_instance():
    """Получить подменю"""
    return await execute_query('SELECT * FROM submenus LIMIT 1')


async def get_dish_instance():
    """Получить блюдо"""
    return await execute_query('SELECT * FROM dishes LIMIT 1')
