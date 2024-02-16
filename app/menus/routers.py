from typing import Any

from fastapi import APIRouter, BackgroundTasks, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.menus.service import menu_service
from app.schemas import Menu, MenuAllOut, MenuIn, MenuListOut, MenuOut

router = APIRouter(
    prefix='/api/v1/menus',
    tags=['menus'],
)


@router.get('', response_model=list[MenuListOut])
async def get_menus_list(
        session: AsyncSession = Depends(get_async_session)
) -> list[MenuListOut] | None | Any:
    """Получить список всех меню"""

    menus_list = await menu_service.get_menus_list(
        session
    )
    return menus_list


@router.post('', response_model=MenuListOut, status_code=201)
async def create_menu(
        background_tasks: BackgroundTasks,
        menu: MenuIn = Body(...),
        session: AsyncSession = Depends(get_async_session)
) -> MenuListOut:
    """Создать меню"""

    new_menu = await menu_service.create_menu(
        menu,
        session,
        background_tasks
    )
    return new_menu


@router.get('/all_menus', response_model=list[MenuAllOut])
async def get_menus_with_submenus_and_dishes(
        session: AsyncSession = Depends(get_async_session)
) -> list[MenuAllOut] | None | Any:
    """Получить список всех меню со всеми связанными подменю и блюдами"""

    result = await menu_service.get_menus_with_submenus_and_dishes(
        session
    )
    return result


@router.get(
    '/{menu_id}',
    response_model=MenuOut,
    responses={404: {'description': 'menu not found'}}
)
async def get_menu(
        menu_id: str,
        session: AsyncSession = Depends(get_async_session)
) -> MenuOut | None | Any:
    """Получить меню по id"""

    menu = await menu_service.get_menu(
        menu_id,
        session
    )
    return menu


@router.patch('/{menu_id}', response_model=MenuListOut)
async def update_menu(
        background_tasks: BackgroundTasks,
        menu_id: str,
        menu: MenuIn = Body(...),
        session: AsyncSession = Depends(get_async_session)
) -> MenuListOut:
    """Обновить меню"""

    result = await menu_service.update_menu(
        menu_id,
        menu,
        session,
        background_tasks
    )
    return result


@router.delete('/{menu_id}', response_model=MenuListOut)
async def delete_menu(
        background_tasks: BackgroundTasks,
        menu_id: str,
        session: AsyncSession = Depends(get_async_session)
) -> type[Menu] | None:
    """Удалить меню"""

    result = await menu_service.delete_menu(
        menu_id,
        session,
        background_tasks
    )
    return result
