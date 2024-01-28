from fastapi import HTTPException
from sqlalchemy import select
from app.models import Menu, Dish


class DishCRUD:

    @classmethod
    async def get_dishes(cls, menu_id, submenu_id, session):
        """Получение всех блюд"""
        query = select(Dish).where(Dish.submenu_id == submenu_id, Menu.id == menu_id)
        result = await session.execute(query)
        dish = result.scalars().all()
        return dish

    @classmethod
    async def create_dish(cls, submenu_id, title, description, price, session):
        """Создание блюда"""
        dish = Dish(
            submenu_id=submenu_id,
            title=title,
            description=description,
            price=price
        )
        session.add(dish)
        await session.commit()
        await session.refresh(dish)
        dish.price = "{:.2f}".format(dish.price)
        return dish

    @classmethod
    async def get_dish(cls, submenu_id, dish_id, session):
        """Получение блюда по id"""
        query = select(Dish).where(Dish.id == dish_id, Dish.submenu_id == submenu_id)
        result = await session.execute(query)
        dish = result.scalars().first()
        if dish is None:
            raise HTTPException(status_code=404, detail="dish not found")
        dish.price = f"{dish.price:.2f}"
        return dish

    @classmethod
    async def update_dish(cls,submenu_id, dish_id, new_title, new_description, new_price, session):
        """Обновление блюда"""
        query = select(Dish).filter_by(id=dish_id, submenu_id=submenu_id)
        result = await session.execute(query)
        dish = result.scalar_one()
        dish.title = new_title
        dish.description = new_description
        dish.price = new_price
        await session.commit()
        dish.price = "{:.2f}".format(dish.price)
        return dish

    @classmethod
    async def delete_dish(cls, dish_id, session):
        """Удаление блюда"""
        query = select(Dish).where(Dish.id == dish_id)
        result = await session.execute(query)
        dish = result.scalars().all()
        for dish in dish:
            await session.delete(dish)
        await session.commit()
