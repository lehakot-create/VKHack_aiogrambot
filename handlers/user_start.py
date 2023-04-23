# Хендлеры по началу общения Юзера с ботом

from datetime import datetime
from datetime import date
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from keyboards.keyboard import yes_no_kb
from keyboards.inline_kb import made_inline_kb
from settings.states import MyState
from data_base.user_data import DBUserData
from settings.config import config, main_menu

async def start_command(message: types.Message, db_user: DBUserData):
    await message.answer(
        f"Добро пожаловать в компанию ООО Ромашка.\n"
        f"Я бот Вася.\n"
        f"Помогу тебе соорентироваться в нашей компании.")

    arg = message.get_args()
    if arg:
        data = await db_user.get_user_data(
            uuid=arg,
            telegram_user_id=message.from_user.id
            )

        if data:
            await message.answer(
                f'Давай сверим данные.\n'
                f'Ты {data.get("surname")} {data.get("name")} {data.get("surname2")}\n'
                f'{data.get("birthday")} г.р.\n'
                f'Должность {data.get("job_title")}\n'
                f'Верно?',
                reply_markup=yes_no_kb())
    await MyState.waiting_check_data.set()



async def process_answer(message: types.Message, db_user: DBUserData, state: FSMContext):
    """
    Обработчик состояния - проверка данных
    """
    if message.text.lower() == 'да':
        # проверка сегодня
        # получаем дату подписания договора из БД
        date_time_contract = await db_user.get_date_time_contract(
            telegram_user_id=str(message.from_user.id)
            )
        # dt0 = datetime.strptime(date_time_contract, '%Y-%m-%d').date()
        dt0 = date_time_contract
        dt1 = date.today()
        if dt1 > dt0:
            await message.answer(
                "Ты уже оформил в отделе кадров документы по приему на работу?",
                reply_markup=yes_no_kb()
            )
            await state.set_state(MyState.waiting_check_date_contract.state)
        else:
            await message.answer(
                f'Оформление твоего трудоустройства назначено на {dt0} в 15.00.\n'
                f'Тебя будут ждать в отделе кадров по адресу: г.Москва, ул.Ленина, 45, оф.215, 2 этаж.\n'
                f'тел 99999999.'
                f'С собой принеси документы:\n'
                f'- паспорт,\n'
                f'- Инн\n'
                f'- трудовая\n'
                f'- диплом и т.д.'
            )
    else:
        await message.answer('Напиши верную информацию и я ее уточню')
        await state.set_state(MyState.waiting_correct_data.state)



async def process_check_date_contract(message: types.Message,
                                      state: FSMContext):
    """
    Обработка ответа на вопрос ты уже оформил документы
    """
    if message.text == 'Да':
        await state.set_state(MyState.info_about_company.state)
        kb = made_inline_kb(main_menu)

        await message.answer(
            "Нажмите на кнопку",
            reply_markup=kb)
    elif message.text == 'Нет':
        await message.answer(
            'тогда тебе неоходимо связаться с отделом кадров по тел. 99999999 для решения этого вопроса.'
            )
    else:
        await message.answer('Нажми либо Да либо Нет')



async def process_send_data_admin(message: types.Message,
                                  state: FSMContext):
    """
    Отправляем данные админу
    """

    bot = message.bot
    await bot.send_message(config.admin_telegram_id,
                           f'Данные на проверку\n'
                           f'{message}')
    await message.answer('Данные направлены админу')



async def process_callback(call: types.CallbackQuery):
    button_data = call.data
    await call.answer(f'{button_data}')




def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(process_answer, state=MyState.waiting_check_data)
    dp.register_message_handler(process_check_date_contract, state=MyState.waiting_check_date_contract)
    dp.register_message_handler(process_send_data_admin, state=MyState.waiting_correct_data)
    dp.register_callback_query_handler(process_callback, lambda callback_query_handler: True)
