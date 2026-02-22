from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    choosing_method = State()
    waiting_for_import = State()
    confirming_data = State()
