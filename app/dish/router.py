from fastapi import APIRouter, Body
from app.dish.crud import DishCRUD
from app.schemas import Dish


router = APIRouter(
    prefix="/api/v1/menus",
    tags=["dishes"],
)


@router.get("/{menu_id}/submenus/{submenu_id}/dishes")
async def get_dishes(menu_id, submenu_id):
    return await DishCRUD.get_dishes(menu_id, submenu_id)


@router.post("/{menu_id}/submenus/{submenu_id}/dishes", status_code=201)
async def create_dish(submenu_id, dish: Dish = Body(...)):
    return await DishCRUD.create_dish(submenu_id, dish.title, dish.description, dish.price)


@router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def get_dish(submenu_id, dish_id):
    return await DishCRUD.get_dish(submenu_id, dish_id)


@router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def update_dish(submenu_id, dish_id, dish: Dish = Body(...)):
    return await DishCRUD.update_dish(submenu_id, dish_id, dish.title, dish.description, dish.price)


@router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def delete_dish(dish_id):
    return await DishCRUD.delete_dish(dish_id)
