from fastapi import HTTPException
from sqlalchemy import select, func
from app.database import async_session_maker
from app.models import Menu, SubMenu, Dish


class MenuCRUD:

    @classmethod
    async def get_menus_list(cls):
        async with async_session_maker() as session:
            query = select(Menu)
            menus = await session.execute(query)
            return menus.scalars().all()

    @classmethod
    async def get_menu(cls, menu_id):
        async with async_session_maker() as session:
            query = select(Menu).filter_by(id=menu_id)
            result = await session.execute(query)
            menu = result.scalars().first()
            if menu is None:
                raise HTTPException(status_code=404, detail="menu not found")
            submenus_count = await session.execute(select(func.count()).where(SubMenu.menu_id == menu.id))
            submenus_count = submenus_count.scalar_one()
            dishes_count = await session.execute(select(func.count()).where(Dish.submenu_id == SubMenu.id))
            dishes_count = dishes_count.scalar_one()
            menu_with_counts = {
                'id': menu.id,
                'title': menu.title,
                'description': menu.description,
                'submenus_count': submenus_count,
                'dishes_count': dishes_count
            }
            return menu_with_counts

    @classmethod
    async def create_menu(cls, title, description):
        async with async_session_maker() as session:
            menu = Menu(title=title, description=description)
            session.add(menu)
            await session.commit()
            await session.refresh(menu)
            return menu

    @classmethod
    async def update_menu(cls, menu_id, new_title, new_description):
        async with async_session_maker() as session:
            query = select(Menu).filter_by(id=menu_id)
            result = await session.execute(query)
            menu = result.scalar_one()
            menu.title = new_title
            menu.description = new_description
            await session.commit()
            return menu

    @classmethod
    async def delete_menu(cls, menu_id):
        async with async_session_maker() as session:
            menu = await session.get(Menu, menu_id)
            await session.delete(menu)
            await session.commit()
            return menu
