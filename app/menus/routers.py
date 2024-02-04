from typing import Any, Sequence

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.menus.service import menu_service
from app.schemas import Menu, MenuIn, MenuOut

router = APIRouter(
    prefix='/api/v1/menus',
    tags=['menus'],
)


@router.get('', response_model=list[MenuOut])
async def get_menus_list(
        session: AsyncSession = Depends(get_async_session)
) -> Sequence[MenuOut] | None | Any:
    """Получить список всех меню"""

    menus_list = await menu_service.get_menus_list(session)
    return menus_list


@router.get(
    '/{menu_id}',
    response_model=MenuOut,
    responses={404: {'description': 'menu not found'}}
)
async def get_menu(
        menu_id: str,
        session: AsyncSession = Depends(get_async_session)
) -> dict[str, str | int] | None | Any:
    """Получить меню по id"""

    menu = await menu_service.get_menu(menu_id, session)
    return menu


@router.post('', response_model=MenuOut, status_code=201)
async def create_menu(
        menu: MenuIn = Body(...),
        session: AsyncSession = Depends(get_async_session)
) -> MenuOut:
    """Создать меню"""

    new_menu = await menu_service.create_menu(menu, session)
    return new_menu


@router.patch('/{menu_id}', response_model=MenuOut)
async def update_menu(
    menu_id: str,
    menu: MenuIn = Body(...),
    session: AsyncSession = Depends(get_async_session)
) -> MenuOut:
    """Обновить меню"""

    result = await menu_service.update_menu(
        menu_id,
        menu,
        session
    )
    return result


@router.delete('/{menu_id}', response_model=MenuOut)
async def delete_menu(
        menu_id: str,
        session: AsyncSession = Depends(get_async_session)
) -> type[Menu] | None:
    """Удалить меню"""

    result = await menu_service.delete_menu(menu_id, session)
    return result
