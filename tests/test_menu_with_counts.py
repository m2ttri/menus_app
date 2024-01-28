from httpx import AsyncClient


async def test_menu_with_counts(ac: AsyncClient):
    """Проверка кол-ва блюд и подменю в меню"""

    # Создаёт меню
    data = {
        "title": "My menu 1",
        "description": "My menu description 1"
    }
    response = await ac.post('/api/v1/menus', json=data)
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert data['title'] == 'My menu 1'
    assert data['description'] == 'My menu description 1'
    menu_id = data['id']

    # Создаёт подменю
    data = {
        'title': 'My submenu 1',
        'description': 'My submenu description 1'
    }
    response = await ac.post(f'/api/v1/menus/{menu_id}/submenus', json=data)
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert data['menu_id'] == str(menu_id)
    assert data['title'] == 'My submenu 1'
    assert data['description'] == 'My submenu description 1'
    submenu_id = data['id']

    #Создаёт блюдо 1
    data = {
        'title': 'My dish 1',
        'description': 'My dish description 1',
        'price': '12.50'
    }
    response = await ac.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=data)
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert data['submenu_id'] == str(submenu_id)
    assert data['title'] == 'My dish 1'
    assert data['description'] == 'My dish description 1'
    assert data['price'] == '12.50'

    # Создаёт блюдо 2
    data = {
        'title': 'My dish 2',
        'description': 'My dish description 2',
        'price': '13.50'
    }
    response = await ac.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=data)
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert data['submenu_id'] == str(submenu_id)
    assert data['title'] == 'My dish 2'
    assert data['description'] == 'My dish description 2'
    assert data['price'] == '13.50'

    # Просматривает определённое блюдо
    response = await ac.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == str(menu_id)
    assert data['title'] == 'My menu 1'
    assert data['description'] == 'My menu description 1'
    assert data['submenus_count'] == 1
    assert data['dishes_count'] == 2

    # Просматривает определённое подменю
    response = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == str(submenu_id)
    assert data['menu_id'] == str(menu_id)
    assert data['title'] == 'My submenu 1'
    assert data['description'] == 'My submenu description 1'
    assert data['dishes_count'] == 2

    # Удаляет подменю
    response = await ac.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200

    # Просматривает список подменю
    response = await ac.get(f'/api/v1/menus/{menu_id}/submenus')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

    # Просматривает список блюд
    response = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

    # Просматривает определённое меню
    response = await ac.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == str(menu_id)
    assert data['title'] == 'My menu 1'
    assert data['description'] == 'My menu description 1'
    assert data['submenus_count'] == 0
    assert data['dishes_count'] == 0

    # Удаляет меню
    response = await ac.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    print(response.json())

    # Просматривает список меню
    response = await ac.get('/api/v1/menus')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0
