from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def yes_no_kb():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_yes = KeyboardButton(text='Да')
    btn_no = KeyboardButton(text='Нет')
    keyboard.add(btn_yes, btn_no)
    return keyboard
