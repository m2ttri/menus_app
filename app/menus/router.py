from fastapi import APIRouter, Body
from app.menus.crud import MenuCRUD
from app.schemas import Menu


router = APIRouter(
    prefix="/api/v1/menus",
    tags=["menus"],
)


@router.get("")
async def get_menus_list():
    return await MenuCRUD.get_menus_list()


@router.get("/{menu_id}")
async def get_menu(menu_id):
    return await MenuCRUD.get_menu(menu_id)


@router.post("", status_code=201)
async def create_menu(menu: Menu = Body(...)):
    return await MenuCRUD.create_menu(menu.title, menu.description)


@router.patch("/{menu_id}")
async def update_menu(menu_id: str, menu: Menu = Body(...)):
    return await MenuCRUD.update_menu(menu_id, menu.title, menu.description)


@router.delete("/{menu_id}")
async def delete_menu(menu_id):
    return await MenuCRUD.delete_menu(menu_id)
