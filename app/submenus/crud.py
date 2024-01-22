from fastapi import HTTPException
from sqlalchemy import select, func
from app.database import async_session_maker
from app.models import Menu, SubMenu, Dish


class SubMenuCRUD:

    @classmethod
    async def get_submenus(cls, menu_id):
        """Получение всех подменю"""
        async with async_session_maker() as session:
            query = select(SubMenu).join(Menu, Menu.id == SubMenu.menu_id).where(Menu.id == menu_id)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add_submenu(cls, menu_id, title, description):
        """Создание подменю"""
        async with async_session_maker() as session:
            submenu = SubMenu(menu_id=menu_id, title=title, description=description)
            session.add(submenu)
            await session.commit()
            await session.refresh(submenu)
            return submenu

    @classmethod
    async def get_submenu(cls, menu_id, submenu_id):
        """Получение подменю по id с подсчётом количества блюд"""
        async with async_session_maker() as session:
            query = select(SubMenu).where(SubMenu.menu_id == menu_id, SubMenu.id == submenu_id)
            result = await session.execute(query)
            submenu = result.scalar_one_or_none()
            if submenu is None:
                raise HTTPException(status_code=404, detail="submenu not found")
            dishes_count = await session.execute(select(func.count()).where(Dish.submenu_id == SubMenu.id))
            dishes_count = dishes_count.scalar_one()
            submenu_with_counts = {
                'id': submenu.id,
                'title': submenu.title,
                'description': submenu.description,
                'dishes_count': dishes_count
            }
            return submenu_with_counts

    @classmethod
    async def update_submenu(cls, menu_id, submenu_id, new_title, new_description):
        """Обновить подменю"""
        async with async_session_maker() as session:
            query = select(SubMenu).where(SubMenu.menu_id == menu_id, SubMenu.id == submenu_id)
            result = await session.execute(query)
            submenu = result.scalar_one_or_none()
            if submenu is None:
                raise ValueError(f"Submenu with id {submenu_id} does not exist")
            submenu.title = new_title
            submenu.description = new_description
            await session.commit()
            return submenu

    @classmethod
    async def delete_submenu(cls, menu_id):
        """Удалить подменю"""
        async with async_session_maker() as session:
            query = select(SubMenu).where(SubMenu.menu_id == menu_id)
            result = await session.execute(query)
            submenu = result.scalars().all()
            for submenu in submenu:
                await session.delete(submenu)
            await session.commit()
