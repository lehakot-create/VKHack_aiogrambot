import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.environ.get('TOKEN_BOT')

DB_USER = os.environ.get('POSTGRES_USER')
DB_PASS = os.environ.get('POSTGRES_PASS')
DB_HOST = os.environ.get('POSTGRES_HOST')
DB_NAME = os.environ.get('POSTGRES_DB')
DB_PORT = os.environ.get('POSTGRES_PORT')
DATABASE_URL = \
    f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

