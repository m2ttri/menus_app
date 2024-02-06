from conftest import get_dish_instance, get_menu_instance, get_submenu_instance
from httpx import AsyncClient

from app.main import reverse


async def test_create_menu(ac: AsyncClient) -> None:
    """Проверка создания меню"""

    data: dict[str, str] = {
        'title': 'My menu 1',
        'description': 'My menu description 1'
    }
    response = await ac.post(
        reverse('create_menu'),
        json=data
    )
    data = response.json()
    assert response.status_code == 201
    assert 'id' in data
    assert data['title'] == 'My menu 1'
    assert data['description'] == 'My menu description 1'


async def test_get_menus_list(ac: AsyncClient) -> None:
    """Проверка получения списка меню"""

    menu = await get_menu_instance()
    if menu is None:
        await test_create_menu(ac)

    response = await ac.get(reverse('get_menus_list'))
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 1


async def test_get_menu(ac: AsyncClient) -> None:
    """Проверка получения меню по id"""

    menu = await get_menu_instance()
    if menu is None:
        await test_create_menu(ac)
        menu = await get_menu_instance()
    menu_id = menu['id']

    response = await ac.get(
        reverse('get_menu',
                menu_id=menu_id)
    )
    data = response.json()
    assert response.status_code == 200
    assert data['id'] == str(menu_id)
    assert data['title'] == 'My menu 1'
    assert data['description'] == 'My menu description 1'


async def test_update_menu(ac: AsyncClient) -> None:
    """Проверка обновления меню"""

    menu = await get_menu_instance()
    if menu is None:
        await test_create_menu(ac)
        menu = await get_menu_instance()
    menu_id = menu['id']

    data: dict[str, str] = {
        'title': 'My updated menu 1',
        'description': 'My updated menu description 1'
    }
    response = await ac.patch(
        reverse('update_menu',
                menu_id=menu_id),
        json=data
    )
    data = response.json()
    assert response.status_code == 200
    assert data['id'] == str(menu_id)
    assert data['title'] == 'My updated menu 1'
    assert data['description'] == 'My updated menu description 1'


async def test_delete_menu(ac: AsyncClient) -> None:
    """Проверка удаления меню"""

    menu = await get_menu_instance()
    if menu is None:
        await test_create_menu(ac)
        menu = await get_menu_instance()
    menu_id = menu['id']

    response = await ac.delete(
        reverse('delete_menu',
                menu_id=menu_id)
    )
    assert response.status_code == 200


async def test_create_submenu(ac: AsyncClient) -> None:
    """Проверка создания подменю"""

    menu = await get_menu_instance()
    if menu is None:
        await test_create_menu(ac)
        menu = await get_menu_instance()
    menu_id = menu['id']

    data: dict[str, str] = {
        'title': 'My submenu 1',
        'description': 'My submenu description 1'
    }
    response = await ac.post(
        reverse('create_submenu',
                menu_id=menu_id),
        json=data
    )
    data = response.json()
    assert response.status_code == 201
    assert 'id' in data
    assert data['title'] == 'My submenu 1'
    assert data['description'] == 'My submenu description 1'


async def test_get_submenus_list(ac: AsyncClient) -> None:
    """Проверка получения списка подменю"""

    submenu = await get_submenu_instance()
    if submenu is None:
        await test_create_submenu(ac)
        submenu = await get_submenu_instance()
    menu_id = submenu['menu_id']

    response = await ac.get(
        reverse('get_submenus_list',
                menu_id=menu_id)
    )
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 1


async def test_get_submenu(ac: AsyncClient) -> None:
    """Проверка получения подменю по id"""

    submenu = await get_submenu_instance()
    if submenu is None:
        await test_create_submenu(ac)
        submenu = await get_submenu_instance()
    menu_id = submenu['menu_id']
    submenu_id = submenu['id']

    response = await ac.get(
        reverse('get_submenu',
                menu_id=menu_id,
                submenu_id=submenu_id)
    )
    data = response.json()
    assert response.status_code == 200
    assert data['id'] == str(submenu_id)
    assert data['title'] == 'My submenu 1'
    assert data['description'] == 'My submenu description 1'


async def test_update_submenu(ac: AsyncClient) -> None:
    """Проверка обновления подменю"""

    submenu = await get_submenu_instance()
    if submenu is None:
        await test_create_submenu(ac)
        submenu = await get_submenu_instance()
    menu_id = submenu['menu_id']
    submenu_id = submenu['id']

    data: dict[str, str] = {
        'title': 'My updated submenu 1',
        'description': 'My updated submenu description 1'
    }
    response = await ac.patch(
        reverse('update_submenu',
                menu_id=menu_id,
                submenu_id=submenu_id),
        json=data
    )
    data = response.json()
    assert response.status_code == 200
    assert data['id'] == str(submenu_id)
    assert data['title'] == 'My updated submenu 1'
    assert data['description'] == 'My updated submenu description 1'


async def test_delete_submenu(ac: AsyncClient) -> None:
    """Проверка удаления подменю"""

    submenu = await get_submenu_instance()
    if submenu is None:
        await test_create_submenu(ac)
        submenu = await get_submenu_instance()
    menu_id = submenu['menu_id']
    submenu_id = submenu['id']

    response = await ac.delete(
        reverse('delete_submenu',
                menu_id=menu_id,
                submenu_id=submenu_id)
    )
    assert response.status_code == 200


async def test_create_dish(ac: AsyncClient) -> None:
    """Проверка создания блюда"""

    dish = await get_dish_instance()
    if dish is None:
        await test_create_submenu(ac)

    submenu = await get_submenu_instance()
    menu_id = submenu['menu_id']
    submenu_id = submenu['id']

    data: dict[str, str] = {
        'title': 'My dish 1',
        'description': 'My dish description 1',
        'price': '12.50'
    }
    response = await ac.post(
        reverse('create_dish',
                menu_id=menu_id,
                submenu_id=submenu_id),
        json=data
    )
    data = response.json()
    assert response.status_code == 201
    assert 'id' in data
    assert data['title'] == 'My dish 1'
    assert data['description'] == 'My dish description 1'
    assert data['price'] == '12.50'


async def test_get_dishes_list(ac: AsyncClient) -> None:
    """Проверка получения списка блюд"""

    dish = await get_dish_instance()
    if dish is None:
        await test_create_dish(ac)

    submenu = await get_submenu_instance()
    menu_id = submenu['menu_id']
    submenu_id = submenu['id']

    response = await ac.get(
        reverse('get_dishes_list',
                menu_id=menu_id,
                submenu_id=submenu_id)
    )
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 1


async def test_get_dish(ac: AsyncClient) -> None:
    """Проверка получения блюда по id"""

    dish = await get_dish_instance()
    if dish is None:
        await test_create_dish(ac)
        dish = await get_dish_instance()

    menu = await get_menu_instance()
    menu_id = menu['id']
    submenu_id = dish['submenu_id']
    dish_id = dish['id']

    response = await ac.get(
        reverse('get_dish',
                menu_id=menu_id,
                submenu_id=submenu_id,
                dish_id=dish_id)
    )
    data = response.json()
    assert response.status_code == 200
    assert data['id'] == str(dish_id)
    assert data['title'] == 'My dish 1'
    assert data['description'] == 'My dish description 1'
    assert data['price'] == '12.50'


async def test_update_dish(ac: AsyncClient) -> None:
    """Проверка обновления блюда"""

    dish = await get_dish_instance()
    if dish is None:
        await test_create_dish(ac)
        dish = await get_dish_instance()
    menu = await get_menu_instance()
    menu_id = menu['id']
    submenu_id = dish['submenu_id']
    dish_id = dish['id']

    data: dict[str, str] = {
        'title': 'My updated dish 1',
        'description': 'My updated dish description 1',
        'price': '14.50'
    }
    response = await ac.patch(
        reverse('update_dish',
                menu_id=menu_id,
                submenu_id=submenu_id,
                dish_id=dish_id),
        json=data
    )
    data = response.json()
    assert response.status_code == 200
    assert data['id'] == str(dish_id)
    assert data['title'] == 'My updated dish 1'
    assert data['description'] == 'My updated dish description 1'
    assert data['price'] == '14.50'


async def test_delete_dish(ac: AsyncClient) -> None:
    """Проверка удаления блюда"""

    dish = await get_dish_instance()
    if dish is None:
        await test_create_dish(ac)
        dish = await get_dish_instance()
    menu = await get_menu_instance()
    menu_id = menu['id']
    submenu_id = dish['submenu_id']
    dish_id = dish['id']

    response = await ac.delete(
        reverse('delete_dish',
                menu_id=menu_id,
                submenu_id=submenu_id,
                dish_id=dish_id)
    )
    assert response.status_code == 200
