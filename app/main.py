from fastapi import FastAPI
from app.menus.router import router as menu_router
from app.submenus.router import router as submenu_router
from app.dish.router import router as dish_router


app = FastAPI()


app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)
