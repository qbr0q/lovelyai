from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from app.bot.states import Registration
from app.bot.handlers.utils import show_profile_preview, update_profile_field
from app.bot.handlers.registration.utils import extract_profile_data, refresh_edit_menu
from app.bot.handlers.constants import GENDER_BUTTONS, GENDER_BUTTON_MAP
from app.core.lexicon import LEXICON
from app.services.ai_service import AIService


router = Router()


@router.message(Registration.waiting_for_import)
async def process_import(message: Message, state: FSMContext, ai_service: AIService):
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

    await state.update_data(profile_data=profile_data)
    await show_profile_preview(state, msg)
    await state.set_state(Registration.confirm_profile)


@router.message(Registration.edit_gender)
async def edit_gender(message: Message, state: FSMContext):
    gender_input = message.text

    if gender_input not in GENDER_BUTTONS:
        await message.answer("Пожалуйста, выбери вариант на кнопках ниже")
        return

    await update_profile_field(state, "gender",
                               GENDER_BUTTON_MAP.get(gender_input))

    await message.answer(
        "Данные обновлены!",
        reply_markup=ReplyKeyboardRemove()
    )

    await refresh_edit_menu(message, state)
    await state.set_state(Registration.confirm_profile)
