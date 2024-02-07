from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Dish, Menu, SubMenu
from app.repository import AbstractMenu


class MenuCRUD(AbstractMenu):
    """Класс предоставляет методы для выполнения CRUD операций над меню"""

    @classmethod
    async def get_menus_list(cls, session: AsyncSession) -> Sequence[Menu]:
        """Получение всех меню"""

        query = select(Menu)
        menu = await session.execute(query)
        return menu.scalars().all()

    @classmethod
    async def get_menu(
            cls,
            menu_id: str,
            session: AsyncSession
    ) -> dict[str, str | int]:
        """Получение меню по id с подсчётом количества подменю и блюд"""

        query = select(Menu).filter_by(id=menu_id)
        result = await session.execute(query)
        menu = result.scalars().first()
        if menu is None:
            raise HTTPException(
                status_code=404,
                detail='menu not found'
            )
        # Реализация вывода количества подменю и блюд для меню через один запрос
        query = (
            select(
                Menu,
                func.count(distinct(SubMenu.id)).label('submenu_count'),
                func.count(distinct(Dish.id)).label('dishes_count')
            )
            .outerjoin(SubMenu, SubMenu.menu_id == Menu.id)
            .outerjoin(Dish, Dish.submenu_id == SubMenu.id)
            .group_by(Menu.id)
            .filter(Menu.id == menu_id)
        )
        result = await session.execute(query)
        menu, submenus_count, dishes_count = result.first()
        menu_with_counts = {
            'id': menu.id,
            'title': menu.title,
            'description': menu.description,
            'submenus_count': submenus_count,
            'dishes_count': dishes_count
        }
        return menu_with_counts

    @classmethod
    async def create_menu(
            cls,
            title: str,
            description: str,
            session: AsyncSession
    ) -> Menu:
        """Создание меню"""

        menu = Menu(title=title, description=description)
        session.add(menu)
        await session.commit()
        await session.refresh(menu)
        return menu

    @classmethod
    async def update_menu(
            cls,
            menu_id: str,
            new_title: str,
            new_description: str,
            session: AsyncSession
    ) -> Menu:
        """Обновление меню"""

        query = select(Menu).filter_by(id=menu_id)
        result = await session.execute(query)
        menu = result.scalar_one()
        menu.title = new_title
        menu.description = new_description
        await session.commit()
        return menu

    @classmethod
    async def delete_menu(
            cls,
            menu_id: str,
            session: AsyncSession
    ) -> type[Menu] | None:
        """Удаление меню"""

        menu = await session.get(Menu, menu_id)
        await session.delete(menu)
        await session.commit()
        return menu

    @classmethod
    async def get_all_submenu_ids_for_menu(
            cls,
            menu_id: str,
            session: AsyncSession
    ) -> list[str]:
        """Получение всех submenu_id для данного menu_id"""

        query = select(SubMenu.id).filter(SubMenu.menu_id == menu_id)
        result = await session.execute(query)
        return [row[0] for row in result.fetchall()]
