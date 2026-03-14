from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.core.utils import Profile
from app.core.lexicon import LEXICON
from app.bot.states import Registration
from app.bot.handlers.utils import show_profile_preview
from app.bot.handlers.message.utils import fill_profile
from app.database.models import User


router = Router()


@router.message(F.text == "Создать анкету")
async def start_import(message: Message, state: FSMContext, user: User):
    if not user:
        await state.update_data(profile_data=Profile())
        await message.answer("Отлично! Давай знакомиться :)")
        await fill_profile(message, state)


@router.message(F.text == LEXICON.button.import_profile)
async def start_import(message: Message, state: FSMContext, user: User):
    if not user:
        await state.set_state(Registration.waiting_for_import)
        await message.answer(LEXICON.state.waiting_import)


@router.message(F.text == "Мой профиль")
async def my_profile(message: Message, state: FSMContext, user: User):
    await show_profile_preview(state, message, user, edit_msg=False)
