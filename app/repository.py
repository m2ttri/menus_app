from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.orm import Session


class AbstractMenu(ABC):
    """Абстрактный класс для меню"""

    @abstractmethod
    def get_menus_list(self, session: Session) -> Any:
        """Получение списка меню"""
        pass

    @abstractmethod
    def get_menu(self, menu_id: str, session: Session) -> Any:
        """Получение меню по id"""
        pass

    @abstractmethod
    def create_menu(self, title: str, description: str, session: Session) -> Any:
        """Создание нового меню"""
        pass

    @abstractmethod
    def update_menu(self, menu_id: str, new_title: str, new_description: str, session: Session) -> Any:
        """Обновление существующего меню"""
        pass

    @abstractmethod
    def delete_menu(self, menu_id: str, session: Session) -> Any:
        """Удаление меню"""
        pass


class AbstractSubMenu(ABC):
    """Абстрактный класс для подменю"""

    @abstractmethod
    def get_submenus(self, menu_id: str, session: Session) -> Any:
        """Получение списка подменю"""
        pass

    @abstractmethod
    def get_submenu(self, menu_id: str, submenu_id: str, session: Session) -> Any:
        """Получение подменю по id"""
        pass

    @abstractmethod
    def create_submenu(self, menu_id: str, title: str, description: str, session: Session) -> Any:
        """Создание нового подменю"""
        pass

    @abstractmethod
    def update_submenu(self, menu_id: str, submenu_id: str, new_title: str, new_description: str,
                       session: Session) -> Any:
        """Обновление существующего подменю"""
        pass

    @abstractmethod
    def delete_submenu(self, menu_id: str, session: Session) -> Any:
        """Удаление подменю"""
        pass


class AbstractDish(ABC):
    """Абстрактный класс для блюд"""

    @abstractmethod
    def get_dishes(self, menu_id: str, submenu_id: str, session: Session) -> Any:
        """Получение списка блюд"""
        pass

    @abstractmethod
    def get_dish(self, submenu_id: str, dish_id: str, session: Session) -> Any:
        """Получение блюда по id"""
        pass

    @abstractmethod
    def create_dish(self, submenu_id: str, title: str, description: str, price: float, session: Session) -> Any:
        """Создание нового блюда"""
        pass

    @abstractmethod
    def update_dish(self, submenu_id: str, dish_id: str, new_title: str, new_description: str, new_price: float,
                    session: Session) -> Any:
        """Обновление существующего блюда"""
        pass

    @abstractmethod
    def delete_dish(self, dish_id: str, session: Session) -> Any:
        """Удаление блюда"""
        pass
