from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.dish.service import dish_service
from app.schemas import DishIn, DishOut

router = APIRouter(
    prefix='/api/v1/menus',
    tags=['dishes'],
)


@router.get('/{menu_id}/submenus/{submenu_id}/dishes', response_model=list[DishOut])
async def get_dishes(
        menu_id: str,
        submenu_id: str,
        session: AsyncSession = Depends(get_async_session)
):
    """Получить список всех блюд"""
    dishes_list = await dish_service.get_dishes(menu_id, submenu_id, session)
    return dishes_list

    # dishes_list = await cache.get('dishes_list')
    # if dishes_list is not None:
    #     return dishes_list
    # else:
    #     dishes_list = await DishCRUD.get_dishes(
    #         menu_id,
    #         submenu_id,
    #         session
    #     )
    #     await cache.set('menus_list', dishes_list, ex=60)
    #     return dishes_list


@router.get(
    '/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    response_model=DishOut,
    responses={404: {'description': 'dish not found'}}
)
async def get_dish(
        submenu_id,
        dish_id,
        session: AsyncSession = Depends(get_async_session)
):
    """Получить блюдо по id"""

    dish = await dish_service.get_dish(submenu_id, dish_id, session)
    return dish

    # result = await DishCRUD.get_dish(submenu_id, dish_id, session)
    # await cache.invalidate(submenu_id)
    # return result


@router.post(
    '/{menu_id}/submenus/{submenu_id}/dishes',
    response_model=DishOut,
    status_code=201
)
async def create_dish(
        submenu_id,
        dish: DishIn = Body(...),
        session: AsyncSession = Depends(get_async_session)
):
    """Создать блюдо"""

    new_dish = await dish_service.create_dish(
        submenu_id,
        dish,
        session
    )
    return new_dish

    # new_dish = await DishCRUD.create_dish(
    #     submenu_id,
    #     dish.title,
    #     dish.description,
    #     dish.price,
    #     session
    # )
    # await cache.set(new_dish.id, new_dish)
    # return new_dish


@router.patch('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=DishOut)
async def update_dish(
        submenu_id,
        dish_id,
        dish: DishIn = Body(...),
        session: AsyncSession = Depends(get_async_session)
):
    """Обновить блюдо"""

    result = await dish_service.update_dish(submenu_id, dish_id, dish, session)
    return result

    # result = await DishCRUD.update_dish(
    #     submenu_id,
    #     dish_id,
    #     dish.title,
    #     dish.description,
    #     dish.price,
    #     session
    # )
    # await cache.invalidate(submenu_id)
    # return result


@router.delete('/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=DishOut)
async def delete_dish(dish_id, session: AsyncSession = Depends(get_async_session)):
    """Удалить блюдо"""

    result = await dish_service.delete_dish(dish_id, session)
    return result

    # result = await DishCRUD.delete_dish(dish_id, session)
    # await cache.invalidate(dish_id)
    # return result

    # return await DishCRUD.delete_dish(dish_id, session)
