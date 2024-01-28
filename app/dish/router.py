from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.dish.crud import DishCRUD
from app.schemas import Dish


router = APIRouter(
    prefix="/api/v1/menus",
    tags=["dishes"],
)


@router.get("/{menu_id}/submenus/{submenu_id}/dishes")
async def get_dishes(
        menu_id,
        submenu_id,
        session: AsyncSession = Depends(get_async_session)):

    """Получить список всех блюд"""

    return await DishCRUD.get_dishes(
        menu_id,
        submenu_id,
        session
    )


@router.post("/{menu_id}/submenus/{submenu_id}/dishes", status_code=201)
async def create_dish(
        submenu_id,
        dish: Dish = Body(...),
        session: AsyncSession = Depends(get_async_session)):

    """Создать блюдо"""

    return await DishCRUD.create_dish(
        submenu_id,
        dish.title,
        dish.description,
        dish.price,
        session
    )


@router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def get_dish(
        submenu_id,
        dish_id,
        session: AsyncSession = Depends(get_async_session)):

    """Получить блюдо по id"""

    return await DishCRUD.get_dish(
        submenu_id,
        dish_id,
        session
    )


@router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def update_dish(
        submenu_id,
        dish_id,
        dish: Dish = Body(...),
        session: AsyncSession = Depends(get_async_session)):

    """Обновить блюдо"""

    return await DishCRUD.update_dish(
        submenu_id,
        dish_id,
        dish.title,
        dish.description,
        dish.price,
        session
    )


@router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def delete_dish(
        dish_id,
        session: AsyncSession = Depends(get_async_session)):

    """Удалить блюдо"""

    return await DishCRUD.delete_dish(
        dish_id,
        session
    )
