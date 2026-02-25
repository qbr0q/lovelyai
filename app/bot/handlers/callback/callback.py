from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.bot.states import Registration
from app.bot.handlers.utils import show_profile_preview, show_editable_profile, \
    get_reply_keyboard

from app.bot.handlers.constants import GENDER_BUTTONS, FIELDS_CONFIG

router = Router()


@router.callback_query(F.data == "edit_profile")
async def edit_profile(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    profile_data = await state.get_value("profile_data")
    profile_ui = show_editable_profile(profile_data)

    await callback.message.edit_text(profile_ui.text,
                                     reply_markup=profile_ui.kb)


@router.callback_query(F.data == "back_to_profile")
async def back_to_profile(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await show_profile_preview(state, callback.message)


@router.callback_query(F.data.in_({"edit_name", "edit_age", "edit_city",
                                   "edit_bio", "edit_gender"}))
async def edit_profile_field(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    callback_data = callback.data
    field = callback.data.replace("edit_", "")
    config = FIELDS_CONFIG[field]

    profile_data = await state.get_value("profile_data")
    current_val = profile_data.get(field)

    if callback_data == "edit_gender":
        rm = get_reply_keyboard(GENDER_BUTTONS)
    else:
        reply_button = ["Оставить текущее" if callback_data == "edit_bio" else current_val]
        rm = get_reply_keyboard(reply_button) if current_val else None

    await state.set_state(config["state"])
    await callback.message.answer(config["text"], reply_markup=rm)
