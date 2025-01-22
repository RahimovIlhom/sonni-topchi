from aiogram.fsm.state import StatesGroup, State


class SetLanguageStates(StatesGroup):
    language = State()
