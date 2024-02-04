from app.cache import cache
from app.dish.crud import DishCRUD
from app.schemas import DishIn


class DishService:
    """Методы для кеширование и выполнение CRUD операций"""

    def __init__(self):
        self.cache = cache
        self.dish = DishCRUD

    async def get_dishes(self, menu_id, submenu_id, session):
        dishes_list = await self.cache.get('dishes_list')
        if dishes_list is not None:
            return dishes_list

        dishes_list = await self.dish.get_dishes(menu_id, submenu_id, session)
        await self.cache.set('menus_list', dishes_list, ex=60)
        return dishes_list

    async def get_dish(self, submenu_id, dish_id, session):

        # result = await self.dish.get_dish(submenu_id, dish_id, session)
        # await cache.invalidate(submenu_id)
        # return result

        dish = await self.cache.get(dish_id)
        if dish:
            return dish

        dish = await self.dish.get_dish(submenu_id, dish_id, session)
        await self.cache.set(submenu_id, dish)
        return dish

    async def create_dish(self, submenu_id, dish: DishIn, session):
        new_dish = await self.dish.create_dish(submenu_id, dish.title, dish.description, dish.price, session)
        await self.cache.set(new_dish.id, new_dish)
        return new_dish

    async def update_dish(self, submenu_id, dish_id, dish: DishIn, session):
        result = await self.dish.update_dish(
            submenu_id,
            dish_id,
            dish.title,
            dish.description,
            dish.price,
            session
        )
        await self.cache.invalidate(submenu_id)
        return result

    async def delete_dish(self, dish_id, session):
        result = await self.dish.delete_dish(dish_id, session)
        await self.cache.invalidate(dish_id)
        return result


dish_service = DishService()
