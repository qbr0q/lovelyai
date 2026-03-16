from aiogram.types import Message, InlineKeyboardButton, \
    KeyboardButton, InputMediaPhoto
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from app.bot.handlers.constants import GENDER_ICON_MAP, GENDER_MAP, \
    GENDER_BUTTONS, FIELDS_CONFIG, INPUT_GENDER_MAP
from app.core.lexicon import LEXICON
from app.core.utils import SimpleObject


def get_reply_keyboard(buttons_data, row_width=2):
    builder = ReplyKeyboardBuilder()

    builder.add(*[KeyboardButton(text=text) for text in buttons_data])
    builder.adjust(row_width)

    return builder.as_markup(resize_keyboard=True)


def get_inline_keyboard(raw_buttons_data, row_width=2):
    builder = InlineKeyboardBuilder()

    buttons_data = [InlineKeyboardButton(text=button_data.title,
                                         callback_data=button_data.callback,
                                         style=button_data.style)
                    for button_data in raw_buttons_data]
    builder.add(*buttons_data)
    builder.adjust(row_width)

    return builder.as_markup()


def get_start_rm():
    buttons = [LEXICON.button.create_profile, LEXICON.button.import_profile]
    reply_markup = get_reply_keyboard(buttons)

    return reply_markup


async def show_profile_preview(state: FSMContext, message: Message, profile_data,
                               has_profile=True):
    # buttons_data = []
    # if not has_profile:
    #     buttons_data.append(
    #         SimpleObject(title=LEXICON.button.save_profile, callback="save_profile",
    #                      style="success")
    #     )
    # else:
    #     buttons_data.append(
    #         SimpleObject(title="Назад к поиску", callback="back_to_search",
    #                      style="success")
    #     )
    # buttons_data.append(
    #     SimpleObject(title=LEXICON.button.edit_profile, callback="edit_profile")
    # )
    # kb = get_reply_keyboard(buttons_data)
    profile_text = get_profile_text(profile_data)
    profile_media = profile_data.media

    if message.media_group_id:
        media_data = get_profile_media(profile_data.media, profile_text)
        menu_mes = await message.answer_media_group(media=media_data)
    elif profile_media:
        media_data = profile_media[-1]
        menu_mes = await message.answer_photo(photo=media_data.file_id,
                                              caption=profile_text)
    else:
        menu_mes = await message.answer(profile_text)

    await state.update_data(menu_id=menu_mes.message_id)


def show_editable_profile(profile_data):
    gender = GENDER_MAP.get(
        profile_data.gender
    )
    msg = f"Пол - {gender or 'Не указан'}\n" \
          f"Имя - {profile_data.name or 'Не указано'}\n" \
          f"Возраст - {profile_data.age or 'Не указан'}\n" \
          f"Город - {profile_data.city or 'Не указан'}\n" \
          f"Описание - {profile_data.bio or 'Не указано'}\n"

    buttons_data = [
        SimpleObject(title="Редактировать пол", callback="edit_gender"),
        SimpleObject(title="Редактировать имя", callback="edit_name"),
        SimpleObject(title="Редактировать возраст", callback="edit_age"),
        SimpleObject(title="Редактировать город", callback="edit_city"),
        SimpleObject(title="Редактировать описание", callback="edit_bio"),
        SimpleObject(title="Назад", callback="back_to_profile", style="danger")
    ]
    kb = get_inline_keyboard(buttons_data)

    return SimpleObject(text=msg, kb=kb)


async def update_profile_field(profile_data, state, message):
    current_state = await state.get_state()
    field = current_state.split("_")[1]
    data_input = message.text

    config = FIELDS_CONFIG.get(field)
    validate = config.validate
    if validate:
        error_message = validate(data_input)
        if error_message:
            await message.answer(error_message)
            return

    if not (field == "bio" and data_input == "Оставить текущее"):
        data_output = data_input if field != "gender" \
            else INPUT_GENDER_MAP.get(data_input)
        setattr(profile_data, field, data_output)
        await state.update_data(profile_data=profile_data)


async def prepare_field_edit(profile_data, field: str):
    current_val = getattr(profile_data, field)
    config = FIELDS_CONFIG.get(field)

    if field == "gender":
        rm = get_reply_keyboard(GENDER_BUTTONS)
    else:
        reply_button = ["Оставить текущее" if field == "bio" else str(current_val)]
        rm = get_reply_keyboard(reply_button) if current_val else None

    return SimpleObject(text=config.text, state=config.state, rm=rm)


def get_profile_text(profile_data):
    header_parts = []

    if profile_data.name:
        header_parts.append(profile_data.name)
    if profile_data.age:
        header_parts.append(str(profile_data.age))

    header_line = ", ".join(header_parts)

    location_line = f"📍 {profile_data.city} ({profile_data.gar_city})"\
        if profile_data.city else ""

    parts = [header_line]
    if location_line:
        parts.append(location_line)
    if profile_data.bio:
        parts.append(f"\n{profile_data.bio}")

    return "\n".join(parts)


def get_profile_media(album, profile_text):
    media_data = []
    for media in album:
        media_data.append(
            InputMediaPhoto(media=media.photo[-1].file_id)
        )
    media_data[0].caption = profile_text
    return media_data
