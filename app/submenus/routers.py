from typing import Any, Sequence

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models import SubMenu
from app.schemas import SubmenuIn, SubmenuOut
from app.submenus.service import submenu_service

router = APIRouter(
    prefix='/api/v1/menus',
    tags=['submenus'],
)


@router.get('/{menu_id}/submenus', response_model=list[SubmenuOut])
async def get_submenus_list(
        menu_id: str,
        session: AsyncSession = Depends(get_async_session)
) -> list[SubmenuOut] | None | Any:
    """Получить список всех подменю"""

    submenus_list = await submenu_service.get_submenus_list(menu_id, session)
    return submenus_list


@router.get(
    '/{menu_id}/submenus/{submenu_id}',
    response_model=SubmenuOut,
    responses={404: {'description': 'submenu not found'}}
)
async def get_submenu(
        menu_id: str,
        submenu_id: str,
        session: AsyncSession = Depends(get_async_session)
) -> SubmenuOut | None | Any:
    """Получчить подменю по id"""

    submenu = await submenu_service.get_submenu(
        menu_id,
        submenu_id,
        session
    )
    return submenu


@router.post(
    '/{menu_id}/submenus',
    response_model=SubmenuOut,
    status_code=201
)
async def create_submenu(
        menu_id: str,
        submenu: SubmenuIn = Body(...),
        session: AsyncSession = Depends(get_async_session)
) -> SubmenuOut:
    """Создать подменю"""

    new_submenu = await submenu_service.create_submenu(
        menu_id,
        submenu,
        session
    )
    return new_submenu


@router.patch('/{menu_id}/submenus/{submenu_id}', response_model=SubmenuOut)
async def update_submenu(
        menu_id: str,
        submenu_id: str,
        submenu: SubmenuIn = Body(...),
        session: AsyncSession = Depends(get_async_session)
) -> SubmenuOut:
    """Обновить подменю"""

    result = await submenu_service.update_submenu(
        menu_id,
        submenu_id,
        submenu,
        session
    )
    return result


@router.delete('/{menu_id}/submenus/{submenu_id}', response_model=SubmenuOut)
async def delete_submenu(
        menu_id: str,
        submenu_id: str,
        session: AsyncSession = Depends(get_async_session)
) -> Sequence[SubMenu] | SubMenu:
    """Удалить подменю"""

    result = await submenu_service.delete_submenu(menu_id, submenu_id, session)
    return result
