from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def made_inline_kb(data: list):
    inline_keyboard = InlineKeyboardMarkup()

    for el in data:
        inline_keyboard.add(InlineKeyboardButton(
            text=el,
            callback_data=el),
                           )
    return inline_keyboard
