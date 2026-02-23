from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    choosing_method = State()
    waiting_for_import = State()
    confirm_profile = State()

    edit_gender = State()
