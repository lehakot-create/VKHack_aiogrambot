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
    # await message.answer(f'Аргументы: {arg}')
    await message.answer(f"Добро пожаловать в компанию ООО Ромашка.\n"
                         f"Я бот Вася.\n"
                         f"Помогу тебе соорентироваться в нашей компании.")

    if data:
        await message.answer(f'Давай сверим данные.\n'
                             f'Ты {data[1]} {data[2]} {data[6]}\n'
                             f'{data[3]} г.р.\n')
    #                          f'Должность {data[5]["name"]}')
        
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

# https://t.me/hack_teams_bot?start=5000
# https://t.me/hack_teams_bot?start=c441eeca-734d-43f1-bde9-5a680d8487cc
