from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import cache
from app.dish.crud import DishCRUD
from app.models import Dish
from app.schemas import DishIn


class DishService:
    """Методы для кеширования CRUD операций блюда"""

    def __init__(self):
        self.cache = cache
        self.dish = DishCRUD

    async def get_dishes(
            self,
            menu_id: str,
            submenu_id: str,
            session: AsyncSession
    ) -> Sequence[Dish] | None | Any:

        dishes_list = await self.cache.get('dishes_list')
        if dishes_list is not None:
            return dishes_list

        dishes_list = await self.dish.get_dishes(
            menu_id,
            submenu_id,
            session
        )
        await self.cache.set('dishes_list', dishes_list, prefix='dish')
        return dishes_list

    async def get_dish(
            self,
            submenu_id: str,
            dish_id: str,
            session: AsyncSession
    ) -> dict[str, str | int] | None | Any:

        dish = await self.cache.get(dish_id, prefix='dish')
        if dish:
            return dish

        dish = await self.dish.get_dish(
            submenu_id,
            dish_id,
            session
        )
        await self.cache.set(submenu_id, dish, prefix='dish')
        return dish

    async def create_dish(
            self,
            submenu_id: str,
            dish: DishIn,
            session: AsyncSession
    ) -> Dish:

        new_dish = await self.dish.create_dish(
            submenu_id,
            dish.title,
            dish.description,
            dish.price,
            session
        )
        await self.cache.set(new_dish.id, new_dish, prefix='dish')
        return new_dish

    async def update_dish(
            self,
            submenu_id: str,
            dish_id: str,
            dish: DishIn,
            session: AsyncSession
    ) -> Dish:

        result = await self.dish.update_dish(
            submenu_id,
            dish_id,
            dish.title,
            dish.description,
            dish.price,
            session
        )
        await self.cache.invalidate(submenu_id, prefix='dish')
        return result

    async def delete_dish(
            self,
            menu_id: str,
            submenu_id: str,
            dish_id: str,
            session: AsyncSession
    ) -> Sequence[Dish] | Dish:

        result = await self.dish.delete_dish(menu_id, submenu_id, dish_id, session)
        await self.cache.invalidate(dish_id, prefix='dish')
        await self.cache.invalidate(submenu_id, prefix='submenu')
        return result


dish_service = DishService()
