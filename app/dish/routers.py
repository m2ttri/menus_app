from typing import Any, Sequence

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.dish.service import dish_service
from app.schemas import Dish, DishIn, DishOut

router = APIRouter(
    prefix='/api/v1/menus',
    tags=['dishes'],
)


@router.get(
    '/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=list[DishOut]
)
async def get_dishes_list(
        menu_id: str,
        submenu_id: str,
        session: AsyncSession = Depends(get_async_session)
) -> list[DishOut] | None | Any:
    """Получить список всех блюд"""
    dishes_list = await dish_service.get_dishes(
        menu_id,
        submenu_id,
        session
    )
    return dishes_list


@router.get(
    '/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=DishOut,
    responses={404: {'description': 'dish not found'}}
)
async def get_dish(
        submenu_id,
        dish_id,
        session: AsyncSession = Depends(get_async_session)
) -> DishOut | None | Any:
    """Получить блюдо по id"""

    dish = await dish_service.get_dish(
        submenu_id,
        dish_id,
        session
    )
    return dish


@router.post(
    '/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=DishOut,
    status_code=201
)
async def create_dish(
        submenu_id,
        dish: DishIn = Body(...),
        session: AsyncSession = Depends(get_async_session)
) -> DishOut:
    """Создать блюдо"""

    new_dish = await dish_service.create_dish(
        submenu_id,
        dish,
        session
    )
    return new_dish


@router.patch(
    '/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=DishOut
)
async def update_dish(
        submenu_id,
        dish_id,
        dish: DishIn = Body(...),
        session: AsyncSession = Depends(get_async_session)
) -> DishOut:
    """Обновить блюдо"""

    result = await dish_service.update_dish(
        submenu_id,
        dish_id,
        dish,
        session
    )
    return result


@router.delete(
    '/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=DishOut
)
async def delete_dish(
        menu_id,
        submenu_id,
        dish_id,
        session: AsyncSession = Depends(get_async_session)
) -> Sequence[Dish] | Dish:
    """Удалить блюдо"""

    result = await dish_service.delete_dish(menu_id, submenu_id, dish_id, session)
    return result
