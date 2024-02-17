import asyncio
import os

import pandas as pd
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

rabbitmq_user = os.getenv('RABBITMQ_USER')
rabbitmq_password = os.getenv('RABBITMQ_PASSWORD')

celery = Celery(
    'menu_app',
    broker=f"amqp://{rabbitmq_user}:{rabbitmq_password}@rabbitmq:5672//"  # noqa: E231
)


def read_excel_file(file_path: str) -> pd.DataFrame:
    """Читает Excel файл и возвращает данные в виде DataFrame"""
    data = pd.read_excel(file_path)
    return data


@celery.task
def update_database():
    print('HELLO FROM DATABASE')
    loop = asyncio.get_event_loop()
    data = loop.run_in_executor(
        None,
        read_excel_file,
        'admin/Menu.xlsx'
    )
    data = loop.run_until_complete(data)
    for row in data.itertuples():
        print(row)


# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(
#         15.0,
#         update_database.s(),
#         name='Run every 15 seconds'
#     )
