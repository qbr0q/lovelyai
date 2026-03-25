from typing import List
import asyncio
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlmodel.ext.asyncio.session import AsyncSession

from app.bot.states import Registration
from app.bot.handlers.utils import show_self_profile, get_search_buttons, process_match_queue
from app.bot.handlers.registration.utils import extract_profile_data, get_gar_city,\
    save_profile, prepare_media, record_media, match_action_mapping, notify_target_user
from app.database.models import User, MatchAction
from app.core.lexicon import LEXICON
from app.services import AIService, GARService, MatchingService


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
    profile_data.media = prepare_media(album, message.photo)
    profile_data.gar_city = get_gar_city(gar_service, profile_data.city)
    profile_data.bio_vector = ai_service.get_embedding(
        profile_data.bio
    )

    await save_profile(session, profile_data, user)
    await show_self_profile(message, state, profile_data)


@router.message(Registration.profile_menu)
async def profile_menu(message: Message, state: FSMContext, user: User,
                       session: AsyncSession, match_service: MatchingService):
    if message.text == LEXICON.button.edit_bio:
        await message.answer(LEXICON.message.edit_bio)
        await state.set_state(Registration.waiting_bio)
    elif message.text == LEXICON.button.edit_media:
        await message.answer(LEXICON.message.edit_media)
        await state.set_state(Registration.waiting_media)
    elif message.text == LEXICON.button.recreate_profile:
        user.clear()
        await session.flush()

        await message.answer(LEXICON.message.recreate_profile)
        await state.set_state(Registration.waiting_self_profile)
    elif message.text == LEXICON.button.find_matches:
        kb = get_search_buttons()
        await message.answer("Ищу подходящие анкеты...", reply_markup=kb)
        await process_match_queue(message, state, user, session, match_service)
        await state.set_state(Registration.match_action)


@router.message(Registration.match_action)
async def match_action(message: Message, state: FSMContext, user: User,
                       session: AsyncSession, match_service: MatchingService):
    if message.text in (LEXICON.button.like, LEXICON.button.dislike):
        target_user = await state.get_value("current_match")
        action = match_action_mapping.get(message.text)
        record = MatchAction(
            from_user_id=user.id,
            to_user_id=target_user.id,
            action=action
        )
        asyncio.create_task(notify_target_user(message.bot, target_user.telegram_id))
        session.add(record)

        await process_match_queue(message, state, user, session, match_service)


@router.message(Registration.waiting_bio)
async def edit_bio(message: Message, state: FSMContext,
                   user: User, ai_service: AIService):
    new_bio = message.text
    if new_bio:
        new_bio_vector = ai_service.get_embedding(new_bio)
        user.bio = new_bio
        user.bio_vector = new_bio_vector

        await show_self_profile(message, state, user)


@router.message(Registration.waiting_media)
async def edit_media(message: Message, state: FSMContext, user: User,
                     session: AsyncSession, album: List[Message] = None):
    media = prepare_media(album, message.photo)
    if media:
        user_media_records = record_media(media, user.id)
        user.media = []
        session.add_all(user_media_records)
        await session.refresh(user)

        await show_self_profile(message, state, user)


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
