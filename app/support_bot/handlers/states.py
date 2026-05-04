from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    waiting_ticket = State()
