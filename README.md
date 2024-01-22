# REST API меню ресторана
Для запуска приложения выполните следующие шаги:

1. Скопируйте репозиторий: git clone https://github.com/m2ttri/menus_app.git
2. Перейдите в папку с проектом и создайте виртуальное окружение: python -m venv venv
3. Активируйте виртуальное окружение:
- для macOS и linux - source venv/Scripts/activate
- для windows - venv/Scripts/activate
4. Обновите менеджер пакетов: python.exe -m pip install --upgrade pip
5. Установите все зависимости: pip install -r requirements.txt
6. В файле .env укажите свои данные для подключения к БД (по умолчанию выставлены стандартные значения предлагаемые при установке postgresql)
7. Примените миграции: alembic upgrade head
8. Запуск проека: uvicorn app.main:app --reload