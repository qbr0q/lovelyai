from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from app.bot.states import Registration
from app.bot.handlers.utils import show_profile_preview, update_profile_field
from app.bot.handlers.registration.utils import extract_profile_data, refresh_edit_menu
from app.bot.handlers.constants import GENDER_BUTTONS, INPUT_GENDER_MAP, \
    STATE_TO_FIELD, FIELDS_CONFIG
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


@router.message(StateFilter(Registration.edit_gender, Registration.edit_name,
                            Registration.edit_age, Registration.edit_city, Registration.edit_bio))
async def edit_profile_field(message: Message, state: FSMContext):
    current_state = await state.get_state()
    field_key = STATE_TO_FIELD.get(current_state)
    data_input = message.text

    config = FIELDS_CONFIG.get(field_key)
    validate = config.get("validate")
    if validate:
        error_message = validate(data_input)
        if error_message:
            await message.answer(error_message)
            return

    if not (current_state == "Registration:edit_bio" and data_input == "Оставить текущее"):
        data_output = data_input if current_state != "Registration:edit_gender" \
            else INPUT_GENDER_MAP.get(data_input)
        await update_profile_field(state, field_key, data_output)

    await message.answer(
        "Данные обновлены!",
        reply_markup=ReplyKeyboardRemove()
    )

    await refresh_edit_menu(message, state)
    await state.set_state(Registration.confirm_profile)
