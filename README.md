REST API меню ресторана
Для запуска приложения выполните следующие шаги:

Скопируйте репозиторий: git clone https://github.com/m2ttri/menus_app.git
Перейдите в папку с проектом и создайте виртуальное окружение: python -m venv venv
Активируйте виртуальное окружение:
для macOS и linux - source venv/Scripts/activate
для windows - venv/Scripts/activate
Обновите менеджер пакетов: python.exe -m pip install --upgrade pip
Установите все зависимости: pip install -r requirements.txt
В файле .env укажите свои данные для подключения к БД (по умолчанию выставлены стандартные значения предлагаемые при установке postgresql)
Примените миграции: alembic upgrade head
Запуск проека: uvicorn app.main:app --reload