from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Dish, Menu, SubMenu
from app.repository import AbstractSubMenu


class SubMenuCRUD(AbstractSubMenu):
    """Класс предоставляет методы для выполнения CRUD операций над подменю"""

    @classmethod
    async def get_submenus(
            cls,
            menu_id: str,
            session: AsyncSession
    ) -> Sequence[Menu]:
        """Получение всех подменю"""

        query = select(SubMenu).join(Menu, Menu.id == SubMenu.menu_id).where(Menu.id == menu_id)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_submenu(
            cls,
            menu_id: str,
            submenu_id: str,
            session: AsyncSession
    ) -> dict[str, str | int]:
        """Получение подменю по id с подсчётом количества блюд"""

        query = select(SubMenu).where(
            SubMenu.menu_id == menu_id,
            SubMenu.id == submenu_id
        )
        result = await session.execute(query)
        submenu = result.scalar_one_or_none()

        if submenu is None:
            raise HTTPException(status_code=404, detail='submenu not found')

        dishes_count = await session.execute(select(func.count()).where(Dish.submenu_id == SubMenu.id))
        dishes_count = dishes_count.scalar_one()
        submenu_with_counts = {
            'id': submenu.id,
            'title': submenu.title,
            'description': submenu.description,
            'dishes_count': dishes_count,
            'menu_id': submenu.menu_id
        }
        return submenu_with_counts

    @classmethod
    async def add_submenu(
            cls,
            menu_id: str,
            title: str,
            description: str,
            session: AsyncSession
    ) -> SubMenu:
        """Создание подменю"""

        submenu = SubMenu(
            menu_id=menu_id,
            title=title,
            description=description
        )
        session.add(submenu)
        await session.commit()
        await session.refresh(submenu)
        return submenu

    @classmethod
    async def update_submenu(
            cls,
            menu_id: str,
            submenu_id: str,
            new_title: str,
            new_description: str,
            session: AsyncSession
    ) -> SubMenu:
        """Обновить подменю"""

        query = select(SubMenu).where(
            SubMenu.menu_id == menu_id,
            SubMenu.id == submenu_id
        )
        result = await session.execute(query)
        submenu = result.scalar_one_or_none()

        if submenu is None:
            raise ValueError(f"Submenu with id {submenu_id} does not exist")

        submenu.title = new_title
        submenu.description = new_description
        await session.commit()
        return submenu

    @classmethod
    async def delete_submenu(
            cls,
            menu_id: str,
            submenu_id: str,
            session: AsyncSession
    ) -> Sequence[SubMenu] | SubMenu:
        """Удалить подменю"""

        query = select(SubMenu).where(SubMenu.menu_id == menu_id)
        result = await session.execute(query)
        submenu = result.scalars().all()
        for submenu in submenu:
            await session.delete(submenu)
        await session.commit()
        return submenu
