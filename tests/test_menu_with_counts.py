from httpx import AsyncClient

from app.main import reverse


async def test_menu_with_counts(ac: AsyncClient) -> None:
    """Проверка кол-ва блюд и подменю в меню"""

    # Создаёт меню
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
    menu_id = data['id']

    # Создаёт подменю
    data = {
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
    submenu_id = data['id']

    # Создаёт блюдо 1
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
    data = response.json()
    assert response.status_code == 201
    assert 'id' in data
    assert data['title'] == 'My dish 1'
    assert data['description'] == 'My dish description 1'
    assert data['price'] == '12.50'

    # Создаёт блюдо 2
    data = {
        'title': 'My dish 2',
        'description': 'My dish description 2',
        'price': '13.50'
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
    assert data['title'] == 'My dish 2'
    assert data['description'] == 'My dish description 2'
    assert data['price'] == '13.50'

    # Просматривает определённое меню
    response = await ac.get(
        reverse('get_menu',
                menu_id=menu_id)
    )
    data = response.json()
    assert response.status_code == 200
    assert data['id'] == str(menu_id)
    assert data['title'] == 'My menu 1'
    assert data['description'] == 'My menu description 1'
    assert data['submenus_count'] == 1
    assert data['dishes_count'] == 2

    # Просматривает определённое подменю
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
    assert data['dishes_count'] == 2

    # Удаляет подменю
    response = await ac.delete(
        reverse('delete_submenu',
                menu_id=menu_id,
                submenu_id=submenu_id)
    )
    assert response.status_code == 200

    # Просматривает список подменю
    response = await ac.get(
        reverse('get_submenus_list',
                menu_id=menu_id)
    )
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 0

    # Просматривает список блюд
    response = await ac.get(
        reverse('get_dishes_list',
                menu_id=menu_id,
                submenu_id=submenu_id)
    )
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 0

    # Просматривает определённое меню
    response = await ac.get(
        reverse('get_menu',
                menu_id=menu_id)
    )
    data = response.json()
    assert response.status_code == 200
    assert data['id'] == str(menu_id)
    assert data['title'] == 'My menu 1'
    assert data['description'] == 'My menu description 1'
    assert data['submenus_count'] == 0
    assert data['dishes_count'] == 0

    # Удаляет меню
    response = await ac.delete(
        reverse('delete_menu',
                menu_id=menu_id)
    )
    assert response.status_code == 200

    # Просматривает список меню
    response = await ac.get(reverse('get_menus_list'))
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 0
