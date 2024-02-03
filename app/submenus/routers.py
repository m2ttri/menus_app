from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import cache
from app.database import get_async_session
from app.schemas import SubmenuIn, SubmenuOut
from app.submenus.service import SubMenuCRUD

router = APIRouter(
    prefix='/api/v1/menus',
    tags=['submenus'],
)


@router.get(
    '/{menu_id}/submenus',
    response_model=list[SubmenuOut]
)
async def get_submenus(
        menu_id: str,
        session: AsyncSession = Depends(get_async_session)
):
    """Получить список всех подменю"""

    submenus_list = await cache.get('submenus_list')
    if submenus_list is not None:
        return submenus_list
    else:
        submenus_list = await SubMenuCRUD.get_submenus(menu_id, session)
        await cache.set(
            'menus_list',
            submenus_list,
            ex=60
        )
        return submenus_list


@router.post(
    '/{menu_id}/submenus',
    response_model=SubmenuOut,
    status_code=201
)
async def create_submenu(
        menu_id: str,
        submenu: SubmenuIn = Body(...),
        session: AsyncSession = Depends(get_async_session)
):
    """Создать подменю"""

    new_submenu = await SubMenuCRUD.add_submenu(
        menu_id,
        submenu.title,
        submenu.description,
        session
    )
    await cache.set(new_submenu.id, new_submenu)
    return new_submenu


@router.get(
    '/{menu_id}/submenus/{submenu_id}',
    response_model=SubmenuOut,
    responses={404: {'description': 'submenu not found'}}
)
async def get_submenu(
        menu_id: str,
        submenu_id: str,
        session: AsyncSession = Depends(get_async_session)
):
    """Получчить подменю по id"""

    submenu = await cache.get(submenu_id)
    if submenu:
        return submenu
    else:
        menu = await SubMenuCRUD.get_submenu(
            menu_id,
            submenu_id,
            session
        )
        await cache.set(menu_id, menu)
        return menu


@router.patch('/{menu_id}/submenus/{submenu_id}', response_model=SubmenuOut)
async def update_submenu(
        menu_id: str,
        submenu_id: str,
        submenu: SubmenuIn = Body(...),
        session: AsyncSession = Depends(get_async_session)
):
    """Обновить подменю"""

    result = await SubMenuCRUD.update_submenu(
        menu_id,
        submenu_id,
        submenu.title,
        submenu.description,
        session
    )
    await cache.invalidate(menu_id)
    return result


@router.delete('/{menu_id}/submenus/{submenu_id}', response_model=SubmenuOut)
async def delete_submenu(menu_id: str, session: AsyncSession = Depends(get_async_session)):
    """Удалить подменю"""

    result = await SubMenuCRUD.delete_submenu(menu_id, session)
    await cache.invalidate(menu_id)
    return result
