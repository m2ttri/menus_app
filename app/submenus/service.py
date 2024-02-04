from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import cache
from app.models import SubMenu
from app.schemas import SubmenuIn
from app.submenus.crud import SubMenuCRUD


class SubmenuService:
    """Методы для кеширование и выполнение CRUD операций"""

    def __init__(self):
        self.cache = cache
        self.submenu = SubMenuCRUD

    async def get_submenus_list(
            self,
            menu_id: str,
            session: AsyncSession
    ) -> Sequence[SubMenu] | None | Any:

        submenus_list = await self.cache.get('submenus_list')
        if submenus_list is not None:
            return submenus_list

        submenus_list = await self.submenu.get_submenus(menu_id, session)
        await self.cache.set('menus_list', submenus_list, ex=60)
        return submenus_list

    async def get_submenu(
            self,
            menu_id: str,
            submenu_id: str,
            session: AsyncSession
    ) -> dict[str, str | int] | None | Any:

        submenu = await self.cache.get(submenu_id)
        if submenu:
            return submenu

        submenu = await self.submenu.get_submenu(
            menu_id,
            submenu_id,
            session
        )
        await self.cache.set(menu_id, submenu)
        return submenu

    async def create_submenu(
            self,
            menu_id: str,
            submenu: SubmenuIn,
            session: AsyncSession
    ) -> SubMenu:

        new_submenu = await self.submenu.add_submenu(
            menu_id,
            submenu.title,
            submenu.description,
            session
        )
        await self.cache.set(new_submenu.id, new_submenu)
        return new_submenu

    async def update_submenu(
            self,
            menu_id: str,
            submenu_id: str,
            submenu: SubmenuIn,
            session: AsyncSession
    ) -> SubMenu:

        result = await self.submenu.update_submenu(
            menu_id,
            submenu_id,
            submenu.title,
            submenu.description,
            session
        )
        await self.cache.invalidate(menu_id)
        return result

    async def delete_submenu(
            self,
            menu_id: str,
            session: AsyncSession
    ) -> Sequence[SubMenu] | SubMenu:

        result = await self.submenu.delete_submenu(menu_id, session)
        await self.cache.invalidate(menu_id)
        return result


submenu_service = SubmenuService()
