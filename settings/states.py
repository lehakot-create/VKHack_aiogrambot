from aiogram.dispatcher.filters.state import State, StatesGroup


class MyState(StatesGroup):
    waiting_check_data = State()
    waiting_correct_data = State()
    waiting_check_date_contract = State()
    info_about_company = State()
