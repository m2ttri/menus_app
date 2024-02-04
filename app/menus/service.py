from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import cache
from app.menus.crud import MenuCRUD
from app.models import Menu
from app.schemas import MenuIn


class MenuService:
    """Методы для кеширования CRUD операций меню"""

    def __init__(self):
        self.cache = cache
        self.menu = MenuCRUD()

    async def get_menus_list(self, session: AsyncSession) -> Sequence[Menu] | None | Any:
        menus_list = await self.cache.get('menus_list')
        if menus_list is not None:
            return menus_list

        menus_list = await self.menu.get_menus_list(session)
        await self.cache.set('menus_list', menus_list, ex=60)
        return menus_list

    async def get_menu(self, menu_id: str, session: AsyncSession) -> dict[str, str | int] | None | Any:
        menu = await self.cache.get(menu_id)
        if menu:
            return menu

        menu = await self.menu.get_menu(menu_id, session)
        await self.cache.set(menu_id, menu)
        return menu

    async def create_menu(self, menu: MenuIn, session: AsyncSession) -> Menu:
        new_menu = await self.menu.create_menu(
            menu.title,
            menu.description,
            session
        )
        await self.cache.set(new_menu.id, new_menu)
        return new_menu

    async def update_menu(self, menu_id: str, menu: MenuIn, session: AsyncSession) -> Menu:
        result = await self.menu.update_menu(
            menu_id,
            menu.title,
            menu.description,
            session
        )
        await self.cache.invalidate(menu_id)
        return result

    async def delete_menu(self, menu_id: str, session: AsyncSession) -> type[Menu] | None:
        result = await self.menu.delete_menu(menu_id, session)
        await self.cache.invalidate(menu_id)
        return result


menu_service = MenuService()
