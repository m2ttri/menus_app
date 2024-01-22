from fastapi import APIRouter, Body
from app.submenus.crud import SubMenuCRUD
from app.schemas import Submenu


router = APIRouter(
    prefix="/api/v1/menus",
    tags=["submenus"],
)


@router.get("/{menu_id}/submenus")
async def get_submenus(menu_id):
    """Получить список всех подменю"""
    return await SubMenuCRUD().get_submenus(menu_id)


@router.post("/{menu_id}/submenus", status_code=201)
async def create_submenu(menu_id, submenu: Submenu = Body(...)):
    """Создать подменю"""
    return await SubMenuCRUD().add_submenu(menu_id, submenu.title, submenu.description)


@router.get("/{menu_id}/submenus/{submenu_id}")
async def get_submenu(menu_id, submenu_id):
    """Получчить подменю по id"""
    return await SubMenuCRUD().get_submenu(menu_id, submenu_id)


@router.patch("/{menu_id}/submenus/{submenu_id}")
async def update_submenu(menu_id: str, submenu_id: str, submenu: Submenu = Body(...)):
    """Обновить подменю"""
    return await SubMenuCRUD().update_submenu(menu_id, submenu_id, submenu.title, submenu.description)


@router.delete("/{menu_id}/submenus/{submenu_id}")
async def delete_submenu(menu_id):
    """Удалить подменю"""
    return await SubMenuCRUD().delete_submenu(menu_id)
