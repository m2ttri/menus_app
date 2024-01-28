from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.menus.crud import MenuCRUD
from app.schemas import Menu


router = APIRouter(
    prefix="/api/v1/menus",
    tags=["menus"],
)


@router.get("")
async def get_menus_list(session: AsyncSession = Depends(get_async_session)):
    """Получить список всех меню"""
    return await MenuCRUD.get_menus_list(session)


@router.get("/{menu_id}")
async def get_menu(menu_id, session: AsyncSession = Depends(get_async_session)):
    """Получить меню по id"""
    return await MenuCRUD.get_menu(menu_id, session)


@router.post("", status_code=201)
async def create_menu(menu: Menu = Body(...),
                      session: AsyncSession = Depends(get_async_session)):
    """Создать меню"""
    return await MenuCRUD.create_menu(menu.title, menu.description, session)


@router.patch("/{menu_id}")
async def update_menu(menu_id: str, menu: Menu = Body(...), session: AsyncSession = Depends(get_async_session)):
    """Обновить меню"""
    return await MenuCRUD.update_menu(menu_id, menu.title, menu.description, session)


@router.delete("/{menu_id}")
async def delete_menu(menu_id, session: AsyncSession = Depends(get_async_session)):
    """Удалить меню"""
    return await MenuCRUD.delete_menu(menu_id, session)
