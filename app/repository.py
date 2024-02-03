from abc import ABC, abstractmethod


class AbstractMenu(ABC):
    @abstractmethod
    def get_menus_list(self, session):
        pass

    @abstractmethod
    def get_menu(self, menu_id, session):
        pass

    @abstractmethod
    def create_menu(self, title, description, session):
        pass

    @abstractmethod
    def update_menu(self, menu_id, new_title, new_description, session):
        pass

    @abstractmethod
    def delete_menu(self, menu_id, session):
        pass


class AbstractSubMenu(ABC):
    @abstractmethod
    def get_submenus(self, menu_id, session):
        pass

    @abstractmethod
    def get_submenu(self, menu_id, submenu_id, session):
        pass

    @abstractmethod
    def create_submenu(self, menu_id, title, description, session):
        pass

    @abstractmethod
    def update_submenu(self, menu_id, submenu_id, new_title, new_description, session):
        pass

    @abstractmethod
    def delete_submenu(self, menu_id, session):
        pass


class AbstractDish(ABC):
    @abstractmethod
    def get_dishes(self, menu_id, submenu_id, session):
        pass

    @abstractmethod
    def get_dish(self, submenu_id, dish_id, session):
        pass

    @abstractmethod
    def create_dish(self, submenu_id, title, description, price, session):
        pass

    @abstractmethod
    def update_dish(self, submenu_id, dish_id, new_title, new_description, new_price, session):
        pass

    @abstractmethod
    def delete_dish(self, dish_id, session):
        pass
