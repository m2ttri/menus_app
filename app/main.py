from typing import Any

from fastapi import FastAPI

from app.cache import cache
from app.database import get_async_session
from app.dish.routers import router as dish_router
from app.menus.routers import router as menu_router
from app.schemas import HealthCheckResponse
from app.submenus.routers import router as submenu_router

app = FastAPI()

app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)


@app.get('/healthcheck', response_model=HealthCheckResponse)
async def healthcheck():

    # Проверка подключения к Redis
    await cache.check_connection()

    # Проверка подключения к базе данных
    async for _ in get_async_session():
        pass

    return {'status': 'Ok'}


def reverse(route_name: str, **path_params: Any) -> str:
    return app.url_path_for(route_name, **path_params)
