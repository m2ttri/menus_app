from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Dish, Menu
from app.repository import AbstractDish


class DishCRUD(AbstractDish):
    """Класс предоставляет методы для выполнения CRUD операций над блюдом"""

    @classmethod
    async def get_dishes(
            cls,
            menu_id: str,
            submenu_id: str,
            session: AsyncSession
    ) -> Sequence[Dish]:
        """Получение всех блюд"""

        query = select(Dish).where(Dish.submenu_id == submenu_id, Menu.id == menu_id)
        result = await session.execute(query)
        dishes = result.scalars().all()
        for dish in dishes:
            dish.price = f'{dish.price:.2f}'  # noqa: E231
        return dishes

    @classmethod
    async def get_dish(
            cls,
            menu_id: str,
            submenu_id: str,
            dish_id: str,
            session: AsyncSession
    ) -> Dish:
        """Получение блюда по id"""
        query = select(Dish).where(Dish.id == dish_id, Dish.submenu_id == submenu_id)
        result = await session.execute(query)
        dish = result.scalars().first()
        if dish is None:
            raise HTTPException(status_code=404, detail='dish not found')
        dish.price = f'{dish.price:.2f}'  # noqa: E231
        return dish

    @classmethod
    async def create_dish(
            cls,
            menu_id: str,
            submenu_id: str,
            title: str,
            description: str,
            price: float,
            session: AsyncSession
    ) -> Dish:
        """Создание блюда"""

        dish = Dish(
            submenu_id=submenu_id,
            title=title,
            description=description,
            price=float(price)
        )
        session.add(dish)
        await session.commit()
        await session.refresh(dish)
        dish.price = f'{dish.price:.2f}'  # noqa: E231
        return dish

    @classmethod
    async def update_dish(
            cls,
            menu_id: str,
            submenu_id: str,
            dish_id: str,
            new_title: str,
            new_description: str,
            new_price: float,
            session: AsyncSession
    ) -> Dish:
        """Обновление блюда"""

        query = select(Dish).filter_by(id=dish_id, submenu_id=submenu_id)
        result = await session.execute(query)
        dish = result.scalar_one()
        dish.title = new_title
        dish.description = new_description
        dish.price = new_price
        await session.commit()
        return dish

    @classmethod
    async def delete_dish(
            cls,
            menu_id: str,
            submenu_id: str,
            dish_id: str,
            session: AsyncSession
    ) -> Sequence[Dish] | Dish:
        """Удаление блюда"""

        query = select(Dish).where(Dish.id == dish_id)
        result = await session.execute(query)
        dish = result.scalars().all()
        for dish in dish:
            dish.price = f'{dish.price:.2f}'  # noqa: E231
            await session.delete(dish)
        await session.commit()
        return dish
