from typing import Any

ROUTES = {
    'create_menu': '/api/v1/menus',
    'get_menus_list': '/api/v1/menus',
    'get_menu': '/api/v1/menus/{menu_id}',
    'update_menu': '/api/v1/menus/{menu_id}',
    'delete_menu': '/api/v1/menus/{menu_id}',
    'create_submenu': '/api/v1/menus/{menu_id}/submenus',
    'get_submenus_list': '/api/v1/menus/{menu_id}/submenus',
    'get_submenu': '/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    'update_submenu': '/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    'delete_submenu': '/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    'create_dish': '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    'get_dishes_list': '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    'get_dish': '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    'update_dish': '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
    'delete_dish': '/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
}


def reverse(route_name: str, **kwargs: Any) -> str:
    """Возвращает URL по имени маршрута"""
    if route_name in ROUTES:
        return ROUTES[route_name].format(**kwargs)
    else:
        raise ValueError(f'{route_name} not found')
