from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.submenus.crud import SubMenuCRUD
from app.schemas import Submenu


router = APIRouter(
    prefix="/api/v1/menus",
    tags=["submenus"],
)


@router.get("/{menu_id}/submenus")
async def get_submenus(
        menu_id,
        session: AsyncSession = Depends(get_async_session)):

    """Получить список всех подменю"""

    return await SubMenuCRUD().get_submenus(
        menu_id,
        session
    )


@router.post("/{menu_id}/submenus", status_code=201)
async def create_submenu(
        menu_id, submenu: Submenu = Body(...),
        session: AsyncSession = Depends(get_async_session)):

    """Создать подменю"""

    return await SubMenuCRUD().add_submenu(
        menu_id,
        submenu.title,
        submenu.description,
        session
    )


@router.get("/{menu_id}/submenus/{submenu_id}")
async def get_submenu(
        menu_id,
        submenu_id,
        session: AsyncSession = Depends(get_async_session)):

    """Получчить подменю по id"""

    return await SubMenuCRUD().get_submenu(
        menu_id,
        submenu_id,
        session
    )


@router.patch("/{menu_id}/submenus/{submenu_id}")
async def update_submenu(
        menu_id: str,
        submenu_id: str,
        submenu: Submenu = Body(...),
        session: AsyncSession = Depends(get_async_session)):

    """Обновить подменю"""

    return await SubMenuCRUD().update_submenu(
        menu_id,
        submenu_id,
        submenu.title,
        submenu.description,
        session
    )


@router.delete("/{menu_id}/submenus/{submenu_id}")
async def delete_submenu(
        menu_id,
        session: AsyncSession = Depends(get_async_session)):

    """Удалить подменю"""

    return await SubMenuCRUD().delete_submenu(
        menu_id,
        session
    )
