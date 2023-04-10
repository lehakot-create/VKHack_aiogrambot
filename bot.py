import logging
from datetime import date
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from settings.config import TOKEN
from data_base.user_data import DBUserData
from keyboards.keyboard import yes_no_kb


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db_user = DBUserData()


class MyState(StatesGroup):
    waiting_check_data = State()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    arg = message.get_args()
    data = await db_user.get_user_data(
        uuid=arg,
        telegram_user_id=message.from_user.id
        )
    await message.answer(
        f"Добро пожаловать в компанию ООО Ромашка.\n"
        f"Я бот Вася.\n"
        f"Помогу тебе соорентироваться в нашей компании.")

    if data:
        await message.answer(
            f'Давай сверим данные.\n'
            f'Ты {data.get("surname")} {data.get("name")} {data.get("surname2")}\n'
            f'{data.get("birthday")} г.р.\n'
            f'Должность {data.get("job_title")}\n'
            f'Верно?',
            reply_markup=yes_no_kb())
    await MyState.waiting_check_data.set()


@dp.message_handler(state=MyState.waiting_check_data)
async def process_answer(message: types.Message, state: FSMContext):
    """
    Обработчик состояния - проверка данных
    """
    if message.text.lower() == 'да':
        # проверка сегодня
        # получаем дату подписания договора из БД
        pass
    else:
        await message.answer('Напиши верную информацию и ее уточню')
        # здесь код отправки данных админу на проверку
        return


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

# https://t.me/hack_teams_bot?start=5000
# https://t.me/hack_teams_bot?start=c441eeca-734d-43f1-bde9-5a680d8487cc
