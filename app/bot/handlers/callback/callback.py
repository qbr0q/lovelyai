from aiogram import Router, F
# from aiogram.types import CallbackQuery
# from aiogram.fsm.context import FSMContext
# from sqlmodel.ext.asyncio.session import AsyncSession
#
# from app.bot.handlers.utils import show_profile_preview, show_editable_profile, \
#     prepare_field_edit, get_reply_keyboard
# from app.database.models import User
# from .utils import save_user
#
#
router = Router()
#
#
# @router.callback_query(F.data == "edit_profile")
# async def edit_profile(callback: CallbackQuery, state: FSMContext, user: User):
#     await callback.answer()
#     profile_data = await state.get_value("profile_data", user)
#     profile_ui = show_editable_profile(profile_data)
#
#     await callback.message.edit_text(profile_ui.text,
#                                      reply_markup=profile_ui.kb)
#
#
# @router.callback_query(F.data == "back_to_profile")
# async def back_to_profile(callback: CallbackQuery, state: FSMContext, user: User):
#     await callback.answer()
#     profile_data = await state.get_value("profile_data", user)
#     await show_profile_preview(state, callback.message,
#                                profile_data, has_profile=bool(user))
#
#
# @router.callback_query(F.data.in_({"edit_name", "edit_age", "edit_city",
#                                    "edit_bio", "edit_gender"}))
# async def edit_profile_field(callback: CallbackQuery, state: FSMContext, user: User):
#     await callback.answer()
#     callback_data = callback.data
#     field = callback_data.replace("edit_", "")
#     profile_data = await state.get_value("profile_data", user)
#
#     field_data = await prepare_field_edit(profile_data, field)
#
#     await state.set_state(field_data.state.edit_state)
#     await callback.message.answer(field_data.text, reply_markup=field_data.rm)
#
#
# @router.callback_query(F.data == "save_profile")
# async def save_profile(callback: CallbackQuery, state: FSMContext,
#                  session: AsyncSession, user: User):
#     await callback.answer()
#
#     profile_data = await state.get_value("profile_data", user)
#     telegram_id = callback.from_user.id
#
#     await save_user(session, profile_data, telegram_id)
#
#     await callback.message.bot.delete_message(
#         callback.message.chat.id, callback.message.message_id
#     )
#
#     buttons = ["Мой профиль", "Мои фильтры"]
#     reply_markup = get_reply_keyboard(buttons)
#     await callback.message.answer("Успешно сохранено!", reply_markup=reply_markup)
