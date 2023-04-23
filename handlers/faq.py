# Ответы на частые вопросы

from aiogram import types, Dispatcher


text_help = """
<b>/start</b> - начало работы
<b>/company</b> - информация о компании
<b>/contact</b> - адрес, телефоны отделов и email
<b>/go_to_company</b> - как добраться
"""

async def help_cmd(message: types.Message):
    global text_help
    await message.answer(text_help)





def register_faq_handlers(dp: Dispatcher):
    dp.register_message_handler(help_cmd, commands=['help'])
