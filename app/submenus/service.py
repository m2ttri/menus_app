from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import cache
from app.models import SubMenu
from app.schemas import SubmenuIn
from app.submenus.crud import SubMenuCRUD


class SubmenuService:
    """Методы для кеширования CRUD операций поодменю"""

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
        await self.cache.set('submenus_list', submenus_list, prefix='submenu')
        return submenus_list

    async def get_submenu(
            self,
            menu_id: str,
            submenu_id: str,
            session: AsyncSession
    ) -> dict[str, str | int] | None | Any:

        submenu = await self.cache.get(submenu_id, parent_id=menu_id, prefix='submenu')
        if submenu:
            return submenu

        submenu = await self.submenu.get_submenu(
            menu_id,
            submenu_id,
            session
        )
        await self.cache.set(submenu_id, submenu, parent_id=menu_id, prefix='submenu')
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
        await self.cache.set(new_submenu.id, new_submenu, parent_id=menu_id, prefix='submenu')
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
        await self.cache.invalidate(submenu_id, parent_id=menu_id, prefix='submenu')
        return result

    async def delete_submenu(
            self,
            menu_id: str,
            submenu_id: str,
            session: AsyncSession
    ) -> Sequence[SubMenu] | SubMenu:

        result = await self.submenu.delete_submenu(menu_id, submenu_id, session)
        await self.cache.invalidate(submenu_id, parent_id=menu_id, prefix='submenu')
        await self.cache.invalidate(menu_id, prefix='menu')
        return result


submenu_service = SubmenuService()
