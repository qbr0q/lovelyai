from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlmodel.ext.asyncio.session import AsyncSession

from app.bot.handlers.utils import show_profile_preview, show_editable_profile, \
    prepare_field_edit
from app.database.models import User


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
    await show_profile_preview(state, callback.message, edit_msg=callback.message)


@router.callback_query(F.data.in_({"edit_name", "edit_age", "edit_city",
                                   "edit_bio", "edit_gender"}))
async def edit_profile_field(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    callback_data = callback.data
    field = callback_data.replace("edit_", "")

    field_data = await prepare_field_edit(field, state)

    await state.set_state(field_data.state.edit_state)
    await callback.message.answer(field_data.text, reply_markup=field_data.rm)


@router.callback_query(F.data == "save_profile")
async def save_profile(callback: CallbackQuery, state: FSMContext,
                 session: AsyncSession):
    await callback.answer()
    try:
        profile_data = await state.get_value("profile_data")
        record = User(
            telegram_id=callback.from_user.id,
            gender=profile_data.get("gender"),
            name=profile_data.get("name"),
            age=int(profile_data.get("age")),
            city=profile_data.get("city"),
            bio=profile_data.get("bio"),
            status="active"
        )
        session.add(record)
        await callback.message.bot.delete_message(
            callback.message.chat.id, callback.message.message_id
        )
        await callback.message.answer("готово")
    except Exception as e:
        pass
