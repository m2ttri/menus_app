from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import cache
from app.database import get_async_session
from app.menus.service import MenuCRUD
from app.schemas import MenuIn, MenuOut

router = APIRouter(
    prefix='/api/v1/menus',
    tags=['menus'],
)


@router.get('', response_model=list[MenuOut])
async def get_menus_list(session: AsyncSession = Depends(get_async_session)):
    """Получить список всех меню"""

    menus_list = await cache.get('menus_list')
    if menus_list is not None:
        return menus_list

    menus_list = await MenuCRUD.get_menus_list(session)
    await cache.set(
        'menus_list',
        menus_list,
        ex=60
    )
    return menus_list


@router.get(
    '/{menu_id}',
    response_model=MenuOut,
    responses={404: {'description': 'menu not found'}}
)
async def get_menu(
        menu_id: str,
        session: AsyncSession = Depends(get_async_session)
):
    """Получить меню по id"""

    menu = await cache.get(menu_id)
    if menu:
        return menu

    menu = await MenuCRUD.get_menu(menu_id, session)
    await cache.set(menu_id, menu)
    return menu


@router.post(
    '',
    response_model=MenuOut,
    status_code=201
)
async def create_menu(
        menu: MenuIn = Body(...),
        session: AsyncSession = Depends(get_async_session)
):
    """Создать меню"""

    new_menu = await MenuCRUD.create_menu(
        menu.title,
        menu.description,
        session
    )
    await cache.set(new_menu.id, new_menu)
    return new_menu


@router.patch('/{menu_id}', response_model=MenuOut)
async def update_menu(
    menu_id: str,
    menu: MenuIn = Body(...),
    session: AsyncSession = Depends(get_async_session)
):
    """Обновить меню"""

    result = await MenuCRUD.update_menu(
        menu_id,
        menu.title,
        menu.description,
        session
    )
    await cache.invalidate(menu_id)
    return result


@router.delete('/{menu_id}', response_model=MenuOut)
async def delete_menu(
        menu_id: str,
        session: AsyncSession = Depends(get_async_session)
):
    """Удалить меню"""

    result = await MenuCRUD.delete_menu(menu_id, session)
    await cache.invalidate(menu_id)
    return result
