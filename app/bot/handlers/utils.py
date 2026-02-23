from types import SimpleNamespace as sn
from aiogram.types import Message, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from app.bot.handlers.constants import GENDER_ICON_MAP, GENDER_MAP
from app.core.lexicon import LEXICON


def get_reply_keyboard(buttons_data, row_width=2):
    builder = ReplyKeyboardBuilder()

    builder.add(*[KeyboardButton(text=text) for text in buttons_data])
    builder.adjust(row_width)

    return builder.as_markup(resize_keyboard=True)


def get_inline_keyboard(raw_buttons_data, row_width=2):
    builder = InlineKeyboardBuilder()
    buttons_data = [InlineKeyboardButton(text=button_data[0], callback_data=button_data[1])
                    for button_data in raw_buttons_data]

    builder.add(*buttons_data)
    builder.adjust(row_width)

    return builder.as_markup()


async def show_profile_preview(state: FSMContext, edit_msg: Message):
    profile_data = await state.get_value("profile_data")

    buttons_data = [
        (LEXICON.button.save_profile, "save_profile"),
        (LEXICON.button.edit_profile, "edit_profile")
    ]
    kb = get_inline_keyboard(buttons_data)

    gender_icon = GENDER_ICON_MAP.get(profile_data.get('gender'), "🤍")
    profile_text = f"{gender_icon} {profile_data.get('name')}, " \
              f"{profile_data.get('age')}, {profile_data.get('city')}\n{profile_data.get('bio')}"

    menu_mes = await edit_msg.edit_text(profile_text, reply_markup=kb)
    await state.update_data(menu_id=menu_mes.message_id)


def show_editable_profile(profile_data):
    gender = GENDER_MAP.get(
        profile_data.get("gender")
    )
    msg = f"Пол - {gender or 'Не указан'}\n" \
          f"Имя - {profile_data.get('name', 'Не указано')}\n" \
          f"Город - {profile_data.get('city', 'Не указан')}\n" \
          f"Описание - {profile_data.get('bio', 'Не указано')}\n"

    buttons_data = [
        ("Редактировать пол", "edit_gender"),
        ("Редактировать имя", "edit_name"),
        ("Редактировать город", "edit_city"),
        ("Редактировать описание", "edit_bio"),
        ("Назад", "back_to_profile")
    ]
    kb = get_inline_keyboard(buttons_data, row_width=1)

    return sn(text=msg, kb=kb)


async def update_profile_field(state: FSMContext, field: str, value: any):
    profile_data = await state.get_value("profile_data") or {}
    profile_data[field] = value
    await state.update_data(profile_data=profile_data)
