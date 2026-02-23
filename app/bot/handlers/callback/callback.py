from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.bot.states import Registration
from app.bot.handlers.utils import show_profile_preview, show_editable_profile, \
    get_reply_keyboard

from app.bot.handlers.constants import GENDER_BUTTONS

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


@router.callback_query(F.data == "edit_gender")
async def edit_gender(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    rm = get_reply_keyboard(GENDER_BUTTONS)
    await state.set_state(Registration.edit_gender)

    await callback.message.answer("Укажи свой пол", reply_markup=rm)
