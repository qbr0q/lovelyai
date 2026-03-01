from aiogram.types import Message, InlineKeyboardButton, KeyboardButton
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


async def show_profile_preview(state: FSMContext, message: Message = None, edit_msg: Message = None):
    profile_data = await state.get_value("profile_data")

    buttons_data = [
        SimpleObject(title=LEXICON.button.save_profile, callback="save_profile",
                     style="success"),
        SimpleObject(title=LEXICON.button.edit_profile, callback="edit_profile")
    ]
    kb = get_inline_keyboard(buttons_data)

    gender_icon = GENDER_ICON_MAP.get(profile_data.get('gender'), "🤍")
    profile_text = f"{gender_icon} {profile_data.get('name')}, " \
              f"{profile_data.get('age')}, {profile_data.get('city')}\n{profile_data.get('bio')}"

    if edit_msg:
        menu_mes = await edit_msg.edit_text(profile_text, reply_markup=kb)
    else:
        menu_mes = await message.answer(profile_text, reply_markup=kb)
    await state.update_data(menu_id=menu_mes.message_id)


def show_editable_profile(profile_data):
    gender = GENDER_MAP.get(
        profile_data.get("gender")
    )
    msg = f"Пол - {gender or 'Не указан'}\n" \
          f"Имя - {profile_data.get('name', 'Не указано')}\n" \
          f"Возраст - {profile_data.get('age', 'Не указан')}\n" \
          f"Город - {profile_data.get('city', 'Не указан')}\n" \
          f"Описание - {profile_data.get('bio', 'Не указано')}\n"

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


async def update_profile_field(state, message):
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
        profile_data = await state.get_value("profile_data", {})
        profile_data[field] = data_output
        await state.update_data(profile_data=profile_data)


async def prepare_field_edit(field, state: FSMContext):
    profile_data = await state.get_value("profile_data", {})
    current_val = profile_data.get(field)
    config = FIELDS_CONFIG.get(field)

    if field == "gender":
        rm = get_reply_keyboard(GENDER_BUTTONS)
    else:
        reply_button = ["Оставить текущее" if field == "bio" else current_val]
        rm = get_reply_keyboard(reply_button) if current_val else None

    return SimpleObject(text=config.text, state=config.state, rm=rm)
