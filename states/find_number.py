from aiogram.fsm.state import StatesGroup, State


class FindNumberStates(StatesGroup):
    game = State()
