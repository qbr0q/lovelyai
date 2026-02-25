from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    choosing_method = State()
    waiting_for_import = State()
    create_profile = State()
    confirm_profile = State()

    # state edit
    edit_gender = State()
    edit_age = State()
    edit_name = State()
    edit_city = State()
    edit_bio = State()
