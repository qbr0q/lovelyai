from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    choosing_method = State()
    waiting_for_import = State()
    confirm_profile = State()

    # create profile
    create_gender = State()
    create_age = State()
    create_name = State()
    create_city = State()
    create_bio = State()

    # edit profile
    edit_gender = State()
    edit_age = State()
    edit_name = State()
    edit_city = State()
    edit_bio = State()
