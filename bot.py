# import logging
from datetime import datetime
from datetime import date
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage



from settings.config import TOKEN, config, main_menu
from settings.settings_commands import set_default_commands
from data_base.user_data import DBUserData
from keyboards.keyboard import yes_no_kb
from keyboards.inline_kb import made_inline_kb

from utils.logger import logger

from handlers.user_start import register_user_handlers
from handlers.faq import register_faq_handlers
from middlewares.db_user import DbMiddleware




async def set_all_commands(bot: Bot):
    await set_default_commands(bot)









# @dp.message_handler(state=MyState.info_about_company)
# async def process_info_menu(message: types.Message,
#                             state: FSMContext):
#     kb = made_inline_kb(main_menu)

#     await message.answer(
#         "Нажмите на кнопку", reply_markup=kb.as_markup())





# @dp.callback_query_handler(text='Режим работы')
# async def process_callback_time_to_work(call: types.CallbackQuery):
#     await call.message.answer('От сих и пока я не скажу...')
#     await call.answer()


# Проверка, что работает, но переделать на структуру папок
# from aiogram.types import BotCommand, BotCommandScopeDefault

# async def set_default_commands(_):
#     await bot.set_my_commands(
#         commands=[
#             BotCommand('help', 'Список всех команд'),
#             BotCommand('company', 'Информация о компании'),
#         ],
#         scope=BotCommandScopeDefault()
#     )

# Регистрация фильтров, хендлеров, миделвари

def register_all_middlewares(dp, db_user):
    dp.setup_middleware(DbMiddleware(db_user))

def register_all_filtres(dp):
    pass

def register_all_handlers(dp: Dispatcher):
    register_user_handlers(dp)
    register_faq_handlers(dp)


async def main():
    bot = Bot(token=TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    db_user = DBUserData()

    register_all_middlewares(dp, db_user)
    register_all_filtres(dp)
    register_all_handlers(dp)

    await set_all_commands(bot)

    try:
        # await executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
        logger.info('Start bot!')
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.close()






if __name__ == '__main__':
    try:
        asyncio.run(main())
        # executor.start_polling(dp, skip_updates=True,
        #                         on_startup=set_default_commands)
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped with error!")
    finally:
        logger.info('Stop bot!')

# https://t.me/hack_teams_bot?start=5000
# https://t.me/hack_teams_bot?start=c441eeca-734d-43f1-bde9-5a680d8487cc
