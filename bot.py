import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from settings.config import TOKEN
from data_base.user_data import DBUserData


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db_user = DBUserData()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    arg = message.get_args()
    data = db_user.get_user_data(arg)
    print(data)
    await message.answer(f'Аргументы: {arg}')
    await message.answer("Привет! Я бот, который может помочь тебе в разных задачах.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

# https://t.me/hack_teams_bot?start=5000