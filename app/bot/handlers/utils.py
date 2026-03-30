from aiogram.types import Message, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from sqlmodel.ext.asyncio.session import AsyncSession

from app.bot.states import Registration
from app.bot.handlers.kb import profile_buttons
from app.database.models import User
from app.services import MatchingService
from app.core.lexicon import LEXICON


async def generic_queue_manager(message: Message, state: FSMContext,
                                key: str, fetch_coro, error_text: str):
    queue = await state.get_value(key)

    if not queue:
        queue = await fetch_coro

    if not queue:
        await message.answer(error_text)
        return

    profile_data = queue.pop(0)

    await state.update_data({
        key: queue,
        f"current_{key}": profile_data
    })

    return profile_data


async def process_match_queue(message: Message, state: FSMContext, user: User,
                              session: AsyncSession, match_service: MatchingService):
    profile_data = await generic_queue_manager(
        message, state, "match_queue",
        match_service.get_match(user, session),
        LEXICON.error.match_over
    )
    if profile_data:
        await show_match_profile(message, profile_data)


async def process_like_queue(message: Message, state: FSMContext, user: User,
                             session: AsyncSession, match_service: MatchingService):
    profile_data = await generic_queue_manager(
        message, state, "match_queue",
        match_service.fetch_received_like(session, user),
        LEXICON.error.match_over
    )
    if profile_data:
        await show_match_profile(message, profile_data)


async def show_self_profile(message: Message, state: FSMContext, profile_data):
    kb = profile_buttons()

    await message.answer(LEXICON.message.current_profile, reply_markup=kb)
    await send_profile_card(message, profile_data)
    await state.set_state(Registration.profile_menu)


async def show_match_profile(message: Message, profile_data):
    await send_profile_card(message, profile_data)


async def send_profile_card(message, profile_data):
    profile_text = get_profile_text(profile_data)
    profile_media = profile_data.media

    if len(profile_media) > 1:
        media_data = get_profile_media(profile_data.media, profile_text)
        await message.answer_media_group(media=media_data)
    elif len(profile_media) == 1:
        media_data = profile_media[0]
        await message.answer_photo(photo=media_data.file_id, caption=profile_text)
    else:
        await message.answer(profile_text)


async def notify_target_user(bot, target_id):
    await bot.send_message(target_id, LEXICON.message.match_notify)


# def show_editable_profile(profile_data):
#     gender = GENDER_MAP.get(
#         profile_data.gender
#     )
#     msg = f"Пол - {gender or 'Не указан'}\n" \
#           f"Имя - {profile_data.name or 'Не указано'}\n" \
#           f"Возраст - {profile_data.age or 'Не указан'}\n" \
#           f"Город - {profile_data.city or 'Не указан'}\n" \
#           f"Описание - {profile_data.bio or 'Не указано'}\n"
#
#     buttons_data = [
#         SimpleObject(title="Редактировать пол", callback="edit_gender"),
#         SimpleObject(title="Редактировать имя", callback="edit_name"),
#         SimpleObject(title="Редактировать возраст", callback="edit_age"),
#         SimpleObject(title="Редактировать город", callback="edit_city"),
#         SimpleObject(title="Редактировать описание", callback="edit_bio"),
#         SimpleObject(title="Назад", callback="back_to_profile", style="danger")
#     ]
#     kb = get_inline_keyboard(buttons_data)
#
#     return SimpleObject(text=msg, kb=kb)


# async def update_profile_field(profile_data, state, message):
#     current_state = await state.get_state()
#     field = current_state.split("_")[1]
#     data_input = message.text
#
#     config = FIELDS_CONFIG.get(field)
#     validate = config.validate
#     if validate:
#         error_message = validate(data_input)
#         if error_message:
#             await message.answer(error_message)
#             return
#
#     if not (field == "bio" and data_input == "Оставить текущее"):
#         data_output = data_input if field != "gender" \
#             else INPUT_GENDER_MAP.get(data_input)
#         setattr(profile_data, field, data_output)
#         await state.update_data(profile_data=profile_data)


# async def prepare_field_edit(profile_data, field: str):
#     current_val = getattr(profile_data, field)
#     config = FIELDS_CONFIG.get(field)
#
#     if field == "gender":
#         rm = get_reply_keyboard(GENDER_BUTTONS)
#     else:
#         reply_button = ["Оставить текущее" if field == "bio" else str(current_val)]
#         rm = get_reply_keyboard(reply_button) if current_val else None
#
#     return SimpleObject(text=config.text, state=config.state, rm=rm)


def get_profile_text(profile_data):
    header_parts = []
    match_percent = ""

    if hasattr(profile_data, "match_percent"):
        match_percent = f"✨{profile_data.match_percent} совместимости\n"
    if profile_data.name:
        header_parts.append(profile_data.name)
    if profile_data.age:
        header_parts.append(str(profile_data.age))

    header_line = ", ".join(header_parts)

    location_line = f"📍 {profile_data.city}" if profile_data.city else ""
    if profile_data.gar_city:
        location_line += f" ({profile_data.gar_city})"

    parts = [match_percent, header_line]
    if location_line:
        parts.append(location_line)
    if profile_data.bio:
        parts.append(f"\n{profile_data.bio}")

    return "\n".join(parts)


def get_profile_media(album, profile_text):
    media_data = []
    for media in album:
        media_data.append(
            InputMediaPhoto(media=media.file_id)
        )
    media_data[0].caption = profile_text
    return media_data
