from typing import List
from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlmodel.ext.asyncio.session import AsyncSession

from app.bot.states import Registration
from app.bot.handlers.utils import show_profile_preview, get_profile_buttons
from app.bot.handlers.registration.utils import extract_profile_data, get_gar_city,\
    save_profile
# from app.bot.handlers.message.utils import fill_profile
# from app.bot.handlers.constants import CREATION_STATE
from app.database.models import User
from app.core.lexicon import LEXICON
from app.services import AIService, GARService


router = Router()


@router.message(Registration.waiting_self_profile)
async def process_import(message: Message, state: FSMContext, ai_service: AIService,
                         gar_service: GARService, session: AsyncSession, user: User,
                         album: List[Message] = None):
    raw_text = message.text or message.caption
    if not raw_text:
        return
    await message.answer(LEXICON.process.import_profile)

    profile_data = await extract_profile_data(ai_service, raw_text)
    profile_data.media = prepare_profile_media(album, message.photo)
    profile_data.gar_city = get_gar_city(gar_service, profile_data.city)
    profile_data.bio_vector = ai_service.get_embedding(
        profile_data.bio
    )
    kb = get_profile_buttons()

    await save_profile(session, profile_data, user)
    await message.answer("Анкета готова!", reply_markup=kb)
    await show_profile_preview(state, message, profile_data)


def prepare_profile_media(album, message_photo):
    if album:
        return [media.photo[-1] for media in album]
    elif message_photo:
        return [message_photo[-1]]
    return []


@router.message(Registration.profile_menu)
async def profile_menu(message: Message):
    pass


# @router.message(StateFilter(Registration.edit_gender, Registration.edit_name,
#                             Registration.edit_age, Registration.edit_city, Registration.edit_bio))
# async def edit_profile_field(message: Message, state: FSMContext, user: User):
#
#     profile_data = await state.get_value("profile_data") or user
#     await update_profile_field(profile_data, state, message)
#
#     await message.answer(
#         "Данные обновлены!",
#         reply_markup=get_start_rm()
#     )
#
#     await refresh_edit_menu(message, state)
#     await state.set_state(Registration.confirm_profile)


# @router.message(StateFilter(Registration.create_gender, Registration.create_name,
#                             Registration.create_age, Registration.create_city, Registration.create_bio))
# async def create_profile_field(message: Message, state: FSMContext, user: User):
#     profile_data = await state.get_value("profile_data", user)
#     await update_profile_field(profile_data, state, message)
#     current_state = await state.get_state()
#
#     try:
#         step = CREATION_STATE.index(current_state)
#         await fill_profile(message, state, step + 1)
#     except Exception as e:
#         rm = get_start_rm()
#         await message.answer("Готово! Анктета сформирована", reply_markup=rm)
#
#         await show_profile_preview(state, message, profile_data,
#                                    edit_msg=False, has_profile=False)
#         await state.set_state(Registration.confirm_profile)
