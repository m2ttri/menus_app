from conftest import get_dish_instance, get_menu_instance, get_submenu_instance
from httpx import AsyncClient
from routes import reverse


async def test_create_menu(ac: AsyncClient):
    """Проверка создания меню"""

    data = {
        'title': 'My menu 1',
        'description': 'My menu description 1'
    }
    response = await ac.post(
        reverse('create_menu'),
        json=data
    )
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert data['title'] == 'My menu 1'
    assert data['description'] == 'My menu description 1'


async def test_get_menus_list(ac: AsyncClient):
    """Проверка получения списка меню"""

    menu = await get_menu_instance()
    if menu is None:
        await test_create_menu(ac)

    response = await ac.get(reverse('get_menus_list'))
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1


async def test_get_menu(ac: AsyncClient):
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
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == str(menu_id)
    assert data['title'] == 'My menu 1'
    assert data['description'] == 'My menu description 1'


async def test_update_menu(ac: AsyncClient):
    """Проверка обновления меню"""

    menu = await get_menu_instance()
    if menu is None:
        await test_create_menu(ac)
        menu = await get_menu_instance()

    menu_id = menu['id']
    data = {
        'title': 'My updated menu 1',
        'description': 'My updated menu description 1'
    }
    response = await ac.patch(
        reverse('update_menu',
                menu_id=menu_id),
        json=data
    )
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == str(menu_id)
    assert data['title'] == 'My updated menu 1'
    assert data['description'] == 'My updated menu description 1'


async def test_delete_menu(ac: AsyncClient):
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


async def test_create_submenu(ac: AsyncClient):
    """Проверка создания подменю"""

    menu = await get_menu_instance()
    if menu is None:
        await test_create_menu(ac)
        menu = await get_menu_instance()

    menu_id = menu['id']
    data = {
        'title': 'My submenu 1',
        'description': 'My submenu description 1'
    }
    response = await ac.post(
        reverse('create_submenu',
                menu_id=menu_id),
        json=data
    )
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert data['title'] == 'My submenu 1'
    assert data['description'] == 'My submenu description 1'


async def test_get_submenus_list(ac: AsyncClient):
    """Проверка получения списка подменю"""

    menu = await get_menu_instance()
    if menu is None:
        await test_create_menu(ac)
        menu = await get_menu_instance()

    menu_id = menu['id']
    response = await ac.get(
        reverse('get_submenus_list',
                menu_id=menu_id)
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1


async def test_get_submenu(ac: AsyncClient):
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
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == str(submenu_id)
    assert data['title'] == 'My submenu 1'
    assert data['description'] == 'My submenu description 1'


async def test_update_submenu(ac: AsyncClient):
    """Проверка обновления подменю"""

    submenu = await get_submenu_instance()
    if submenu is None:
        await test_create_submenu(ac)
        submenu = await get_submenu_instance()

    menu_id = submenu['menu_id']
    submenu_id = submenu['id']
    data = {
        'title': 'My updated submenu 1',
        'description': 'My updated submenu description 1'
    }
    response = await ac.patch(
        reverse('update_submenu',
                menu_id=menu_id,
                submenu_id=submenu_id),
        json=data
    )
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == str(submenu_id)
    assert data['title'] == 'My updated submenu 1'
    assert data['description'] == 'My updated submenu description 1'


async def test_delete_submenu(ac: AsyncClient):
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


async def test_create_dish(ac: AsyncClient):
    """Проверка создания блюда"""

    submenu = await get_submenu_instance()
    if submenu is None:
        await test_create_submenu(ac)
        submenu = await get_submenu_instance()

    menu_id = submenu['menu_id']
    submenu_id = submenu['id']
    data = {
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
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert data['title'] == 'My dish 1'
    assert data['description'] == 'My dish description 1'
    assert data['price'] == '12.50'


async def test_get_dishes_list(ac: AsyncClient):
    """Проверка получения списка блюд"""

    submenu = await get_submenu_instance()
    if submenu is None:
        await test_create_submenu(ac)
        submenu = await get_submenu_instance()

    menu_id = submenu['menu_id']
    submenu_id = submenu['id']
    response = await ac.get(
        reverse('get_dishes_list',
                menu_id=menu_id,
                submenu_id=submenu_id)
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1


async def test_get_dish(ac: AsyncClient):
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
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == str(dish_id)
    assert data['title'] == 'My dish 1'
    assert data['description'] == 'My dish description 1'
    assert data['price'] == '12.50'


async def test_update_dish(ac: AsyncClient):
    """Проверка обновления блюда"""

    dish = await get_dish_instance()
    if dish is None:
        await test_create_dish(ac)
        dish = await get_dish_instance()

    menu = await get_menu_instance()
    menu_id = menu['id']
    submenu_id = dish['submenu_id']
    dish_id = dish['id']
    data = {
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
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == str(dish_id)
    assert data['title'] == 'My updated dish 1'
    assert data['description'] == 'My updated dish description 1'
    assert data['price'] == '14.50'


async def test_delete_dish(ac: AsyncClient):
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
