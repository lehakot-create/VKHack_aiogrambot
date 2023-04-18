import os
from dotenv import load_dotenv
from dataclasses import dataclass


load_dotenv()

TOKEN = os.environ.get('TOKEN_BOT')

DB_USER = os.environ.get('POSTGRES_USER')
DB_PASS = os.environ.get('POSTGRES_PASS')
DB_HOST = os.environ.get('POSTGRES_HOST')
DB_NAME = os.environ.get('POSTGRES_DB')
DB_PORT = os.environ.get('POSTGRES_PORT')
DATABASE_URL = \
    f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


@dataclass
class Config:
    admin_telegram_id: str = os.environ.get('ADMIN_TELEGRAM')


config = Config()


main_menu = [
    'Режим работы',
    'Как добраться',
    'Информация о компании',
    'Структура компании',
    'Внутренние правила',
    'Должностная инструкция',
    'ФИО и контакты начальника отдела',
    'ФИО и контакты наставника',
]
