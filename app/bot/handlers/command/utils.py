from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_reply_keyboard(buttons, row_width=2):
    builder = ReplyKeyboardBuilder()

    for text in buttons:
        builder.add(KeyboardButton(text=text))

    builder.adjust(row_width)

    return builder.as_markup(resize_keyboard=True)
