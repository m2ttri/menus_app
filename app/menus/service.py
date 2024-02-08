from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache import cache
from app.menus.crud import MenuCRUD
from app.models import Menu
from app.schemas import MenuAllOut, MenuIn
from app.submenus.crud import SubMenuCRUD


class MenuService:
    """Методы для кеширования CRUD операций меню"""

    def __init__(self):
        self.cache = cache
        self.menu = MenuCRUD()

    async def get_menus_list(
            self,
            session: AsyncSession
    ) -> Sequence[Menu] | None | Any:

        menus_list = await self.cache.get(
            'menus_list',
            prefix='menu'
        )
        if menus_list is not None:
            return menus_list

        menus_list = await self.menu.get_menus_list(session)

        await self.cache.set(
            'menus_list',
            menus_list,
            prefix='menu'
        )
        return menus_list

    async def get_menu(
            self,
            menu_id: str,
            session: AsyncSession
    ) -> dict[str, str | int] | None | Any:

        menu = await self.cache.get(
            menu_id,
            prefix='menu'
        )
        if menu:
            return menu

        menu = await self.menu.get_menu(
            menu_id,
            session
        )
        await self.cache.set(
            menu_id,
            menu,
            prefix='menu'
        )
        return menu

    async def create_menu(
            self,
            menu: MenuIn,
            session: AsyncSession
    ) -> Menu:
        new_menu = await self.menu.create_menu(
            menu.title,
            menu.description,
            session
        )
        await self.cache.set(
            new_menu.id,
            new_menu,
            prefix='menu'
        )
        return new_menu

    async def update_menu(
            self,
            menu_id: str,
            menu: MenuIn,
            session: AsyncSession
    ) -> Menu:
        result = await self.menu.update_menu(
            menu_id,
            menu.title,
            menu.description,
            session
        )
        await self.cache.invalidate(
            menu_id,
            prefix='menu'
        )
        return result

    async def delete_menu(
            self,
            menu_id: str,
            session: AsyncSession
    ) -> type[Menu] | None:

        submenu_ids = await self.menu.get_all_submenu_ids_for_menu(
            menu_id,
            session
        )
        for submenu_id in submenu_ids:
            dish_ids = await SubMenuCRUD.get_all_dish_ids_for_submenu(
                submenu_id,
                session
            )
            for dish_id in dish_ids:
                await self.cache.invalidate(
                    dish_id,
                    parent_id=submenu_id,
                    prefix='dish'
                )
            await self.cache.invalidate(
                submenu_id,
                parent_id=menu_id,
                prefix='submenu'
            )

        result = await self.menu.delete_menu(
            menu_id,
            session
        )
        await self.cache.invalidate(
            menu_id,
            prefix='menu'
        )
        return result

    async def get_menus_with_submenus_and_dishes(
            self,
            session: AsyncSession
    ) -> list[MenuAllOut] | None | Any:

        menus_out = await self.cache.get(
            'menus_out',
            prefix='menu'
        )
        if menus_out is not None:
            return menus_out

        menus_out = await self.menu.get_menus_with_submenus_and_dishes(
            session
        )
        await self.cache.set(
            'menus_out',
            menus_out,
            prefix='menu'
        )
        return menus_out


menu_service = MenuService()
