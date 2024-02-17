from typing import Any, Sequence

from fastapi import BackgroundTasks
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

        submenus_list = await self.cache.get(
            menu_id,
            prefix='submenu_list'
        )
        if submenus_list is not None:
            return submenus_list

        submenus_list = await self.submenu.get_submenus(
            menu_id,
            session
        )
        await self.cache.set(
            menu_id,
            submenus_list,
            prefix='submenu_list'
        )
        return submenus_list

    async def get_submenu(
            self,
            menu_id: str,
            submenu_id: str,
            session: AsyncSession
    ) -> dict[str, str | int] | None | Any:

        submenu = await self.cache.get(
            submenu_id,
            parent_id=menu_id,
            prefix='submenu'
        )
        if submenu:
            return submenu

        submenu = await self.submenu.get_submenu(
            menu_id,
            submenu_id,
            session
        )
        await self.cache.set(
            submenu_id,
            submenu,
            parent_id=menu_id,
            prefix='submenu'
        )
        return submenu

    async def create_submenu(
            self,
            menu_id: str,
            submenu: SubmenuIn,
            session: AsyncSession,
            background_tasks: BackgroundTasks
    ) -> SubMenu:

        new_submenu = await self.submenu.add_submenu(
            menu_id,
            submenu.title,
            submenu.description,
            session
        )
        await self.cache.set(
            new_submenu.id,
            new_submenu,
            parent_id=menu_id,
            prefix='submenu'
        )
        background_tasks.add_task(
            cache.invalidate,
            'submenus_out',
            None,
            prefix='submenu'
        )
        background_tasks.add_task(
            cache.set,
            'dirty',
            True,
            parent_id=new_submenu.id,
            prefix='submenu',
            ex=60
        )
        return new_submenu

    async def update_submenu(
            self,
            menu_id: str,
            submenu_id: str,
            submenu: SubmenuIn,
            session: AsyncSession,
            background_tasks: BackgroundTasks
    ) -> SubMenu:

        result = await self.submenu.update_submenu(
            menu_id,
            submenu_id,
            submenu.title,
            submenu.description,
            session
        )
        background_tasks.add_task(
            cache.invalidate,
            submenu_id,
            parent_id=menu_id,
            prefix='submenu'
        )
        background_tasks.add_task(
            cache.set,
            'dirty',
            True,
            parent_id=submenu_id,
            prefix='submenu',
            ex=60
        )
        return result

    async def delete_submenu(
            self,
            menu_id: str,
            submenu_id: str,
            session: AsyncSession,
            background_tasks: BackgroundTasks
    ) -> Sequence[SubMenu] | SubMenu:

        dish_ids = await self.submenu.get_all_dish_ids_for_submenu(
            submenu_id,
            session
        )
        for dish_id in dish_ids:
            background_tasks.add_task(
                cache.invalidate,
                dish_id,
                parent_id=submenu_id,
                prefix='dish'
            )
            background_tasks.add_task(
                cache.set,
                'dirty',
                True,
                parent_id=dish_id,
                prefix='dish',
                ex=60
            )
        result = await self.submenu.delete_submenu(
            menu_id,
            submenu_id,
            session
        )
        background_tasks.add_task(
            cache.invalidate,
            submenu_id,
            parent_id=menu_id,
            prefix='submenu'
        )
        background_tasks.add_task(
            cache.set,
            'dirty',
            True,
            parent_id=submenu_id,
            prefix='submenu',
            ex=60
        )
        return result


submenu_service = SubmenuService()
