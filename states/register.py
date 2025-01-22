from aiogram.fsm.state import StatesGroup, State


class RegisterStates(StatesGroup):
    chat_lang = State()
    fullname = State()
    phone = State()
    location = State()
