from typing import Any

from fastapi import FastAPI

from app.dish.routers import router as dish_router
from app.menus.routers import router as menu_router
from app.submenus.routers import router as submenu_router

app = FastAPI()

app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)


def reverse(route_name: str, **path_params: Any) -> str:
    return app.url_path_for(route_name, **path_params)
