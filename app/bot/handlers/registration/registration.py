from typing import List
from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot.states import Registration
from app.bot.handlers.utils import show_profile_preview, update_profile_field, get_start_rm
from app.bot.handlers.registration.utils import extract_profile_data, refresh_edit_menu
from app.bot.handlers.message.utils import fill_profile
from app.bot.handlers.constants import CREATION_STATE
from app.database.models import User
from app.core.lexicon import LEXICON
from app.services import AIService


router = Router()


@router.message(Registration.waiting_for_import)
async def process_import(message: Message, state: FSMContext, ai_service: AIService,
                         album: List[Message] = None):
    if not (message.forward_from_chat or message.forward_from):
        await message.answer(LEXICON.error.message_not_forwared)
        return

    if not message.forward_from.is_bot:
        await message.answer(LEXICON.error.message_forwared_not_from_bot)
        return

    raw_text = message.text or message.caption
    if not raw_text:
        return
    msg = await message.answer(LEXICON.process.import_profile)
    profile_data = await extract_profile_data(ai_service, raw_text)
    profile_data.media = album

    await state.update_data(profile_data=profile_data)
    await show_profile_preview(state, msg, profile_data, has_profile=False)
    await state.set_state(Registration.confirm_profile)


@router.message(StateFilter(Registration.edit_gender, Registration.edit_name,
                            Registration.edit_age, Registration.edit_city, Registration.edit_bio))
async def edit_profile_field(message: Message, state: FSMContext, user: User):

    profile_data = await state.get_value("profile_data") or user
    await update_profile_field(profile_data, state, message)

    await message.answer(
        "Данные обновлены!",
        reply_markup=get_start_rm()
    )

    await refresh_edit_menu(message, state)
    await state.set_state(Registration.confirm_profile)


@router.message(StateFilter(Registration.create_gender, Registration.create_name,
                            Registration.create_age, Registration.create_city, Registration.create_bio))
async def create_profile_field(message: Message, state: FSMContext, user: User):
    profile_data = await state.get_value("profile_data", user)
    await update_profile_field(profile_data, state, message)
    current_state = await state.get_state()

    try:
        step = CREATION_STATE.index(current_state)
        await fill_profile(message, state, step + 1)
    except Exception as e:
        rm = get_start_rm()
        await message.answer("Готово! Анктета сформирована", reply_markup=rm)

        await show_profile_preview(state, message, profile_data,
                                   edit_msg=False, has_profile=False)
        await state.set_state(Registration.confirm_profile)
