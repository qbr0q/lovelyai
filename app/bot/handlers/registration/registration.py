import asyncio
from typing import List
from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core import settings, LEXICON
from app.bot.states import Registration
from app.bot.handlers.utils import show_self_profile, notify_target_user, \
    user_link, is_subscribed
from app.bot.handlers.kb import account_buttons, filter_buttons, channel_buttons
from app.bot.handlers.registration.utils import extract_profile_data, \
    save_profile, prepare_media, record_media
from app.bot.handlers.registration.queue_profile import process_match_queue,\
    process_like_queue, queue_config, match_action_mapping
from app.database.models import User, MatchAction
from app.database.enums import UserStatus, QueueName
from app.services import AIService, GARService, MatchingService
from app.services.ai_service.utils import LimitToken


router = Router()


@router.message(Registration.waiting_self_profile)
async def process_import(message: Message, state: FSMContext, ai_service: AIService,
                         gar_service: GARService, session: AsyncSession, user: User,
                         album: List[Message] = None):
    raw_text = message.text or message.caption
    if len(raw_text.strip()) < 40:
        await message.answer(LEXICON.error.short_input)
        return
    await message.answer(LEXICON.process.import_profile)

    try:
        profile_data = await extract_profile_data(ai_service, raw_text, user.id)
        profile_data.media = prepare_media(album, message.photo)
        profile_data.gar_city = gar_service.fetch_gar_city(profile_data.city)
        profile_data.bio_vector = ai_service.get_embedding(
            profile_data.bio
        )

        user.clear()
        await save_profile(session, profile_data, user)
        await show_self_profile(message, state, profile_data)
    except LimitToken as e:
        await message.answer(str(e))
        await state.set_state(Registration.profile_menu)


@router.message(Registration.profile_menu)
async def profile_menu(message: Message, state: FSMContext, user: User,
                       session: AsyncSession, match_service: MatchingService):
    message_text = message.text
    if message_text == LEXICON.button.edit_bio:
        await message.answer(LEXICON.message.edit_bio)
        await state.set_state(Registration.waiting_bio)
    elif message_text == LEXICON.button.edit_media:
        await message.answer(LEXICON.message.edit_media)
        await state.set_state(Registration.waiting_media)
    elif message_text == LEXICON.button.recreate_profile:
        await message.answer(LEXICON.message.recreate_profile)
        await state.set_state(Registration.waiting_self_profile)
    elif message_text == LEXICON.button.find_matches:
        if not await is_subscribed(message.bot, user.telegram_id, settings.channel.id):
            await message.answer("Подпишись на канал, чтобы открыть доступ к анкетам. 🚀\n\n"
                                 "Это займет пару секунд.", reply_markup=channel_buttons())
            return
        user.status = UserStatus.active

        await message.answer(LEXICON.process.search_match)
        await process_match_queue(message, state, user, session, match_service)
    elif message_text == LEXICON.button.manage_account:
        kb = account_buttons()

        await state.set_state(Registration.manage_account)
        await message.answer(LEXICON.message.account, reply_markup=kb)


@router.message(StateFilter(
    Registration.match_action, Registration.received_like_action
))
async def reaction_action(message: Message, state: FSMContext, user: User,
                          session: AsyncSession, match_service: MatchingService):
    message_text = message.text
    if message_text == LEXICON.button.account:
        kb = account_buttons()

        await state.set_state(Registration.manage_account)
        await message.answer(LEXICON.message.account, reply_markup=kb)

    if message_text not in (LEXICON.button.like, LEXICON.button.dislike):
        return

    current_state = await state.get_state()
    action = match_action_mapping.get(message_text)
    is_like = message_text == LEXICON.button.like
    config = queue_config.get(current_state)

    target_user = await state.get_value(config.key)
    if not target_user:
        return

    if config.key == QueueName.CURRENT_MATCH:
        record = MatchAction(
            from_user_id=user.id,
            to_user_id=target_user.id,
            action=action
        )
        session.add(record)
    elif config.key == QueueName.CURRENT_RECEIVED_LIKE:
        current_match = await match_service.fetch_current_match(
            session, from_user_id=target_user.id, to_user_id=user.id
        )
        current_match.is_match = is_like

    if is_like:
        if config.key == QueueName.CURRENT_MATCH:
            asyncio.create_task(
                notify_target_user(message.bot, target_user.telegram_id, config.msg)
            )
        else:
            await asyncio.gather(
                notify_target_user(message.bot, target_user.telegram_id,
                                   config.msg % user_link(user)),
                notify_target_user(message.bot, user.telegram_id,
                                   config.msg % user_link(target_user)),
                return_exceptions=True
            )

    await config.process_queue(message, state, user, session, match_service)


@router.message(Registration.manage_account)
async def manage_account(message: Message, state: FSMContext, session: AsyncSession,
                         user: User, match_service: MatchingService):
    message_text = message.text
    if message_text == LEXICON.button.profile:
        await show_self_profile(message, state, user)
    elif message_text == LEXICON.button.profile:
        pass
    elif message_text == LEXICON.button.likes:
        await message.answer(LEXICON.process.search_like)
        await process_like_queue(message, state, user, session, match_service)
    # elif message_text == LEXICON.button.filters:
    #     await state.set_state(Registration.filter_manage)
    #     await message.answer("фильтры", reply_markup=filter_buttons())


@router.message(Registration.filter_manage)
async def filter_manage():
    pass


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
