from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    waiting_self_profile = State()
    profile_menu = State()
    waiting_bio = State()
    waiting_media = State()
    match_action = State()
    received_like_action = State()
    manage_account = State()

    # create profile
    # create_gender = State()
    # create_age = State()
    # create_name = State()
    # create_city = State()
    # create_bio = State()

    # edit profile
    # edit_gender = State()
    # edit_age = State()
    # edit_name = State()
    # edit_city = State()
    # edit_bio = State()
