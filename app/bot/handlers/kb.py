from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.core import settings, LEXICON
from app.core.utils import SimpleObject


def get_reply_keyboard(buttons_data, row_width=2):
    builder = ReplyKeyboardBuilder()

    builder.add(*[KeyboardButton(
        text=button_data.title,
        style=button_data.style
    ) for button_data in buttons_data])
    builder.adjust(row_width)

    return builder.as_markup(resize_keyboard=True)


def get_inline_keyboard(raw_buttons_data, row_width=2):
    builder = InlineKeyboardBuilder()

    buttons_data = [InlineKeyboardButton(text=button_data.title,
                                         callback_data=button_data.callback,
                                         url=button_data.url,
                                         style=button_data.style)
                    for button_data in raw_buttons_data]
    builder.add(*buttons_data)
    builder.adjust(row_width)

    return builder.as_markup()


def profile_buttons():
    buttons_data = [
        SimpleObject(title=LEXICON.button.find_matches, style="success"),
        SimpleObject(title=LEXICON.button.recreate_profile, style="danger"),
        SimpleObject(title=LEXICON.button.edit_bio),
        SimpleObject(title=LEXICON.button.edit_media),
        SimpleObject(title=LEXICON.button.manage_account, style="primary")
    ]
    return get_reply_keyboard(buttons_data)


def action_buttons():
    buttons_data = [
        SimpleObject(title=LEXICON.button.like, style="success"),
        SimpleObject(title=LEXICON.button.dislike, style="danger"),
        SimpleObject(title=LEXICON.button.account, style="primary")
    ]
    return get_reply_keyboard(buttons_data, row_width=3)


def account_buttons():
    buttons_data = [
        SimpleObject(title=LEXICON.button.profile),
        SimpleObject(title=LEXICON.button.filters),
        SimpleObject(title=LEXICON.button.likes)
    ]
    return get_reply_keyboard(buttons_data, row_width=3)


def filter_buttons():
    buttons_data = [
        SimpleObject(title="Что я ищу"),
        SimpleObject(title="Что я не ищу")
    ]
    return get_reply_keyboard(buttons_data)


def channel_buttons():
    buttons_data = [
        SimpleObject(title="Подписаться на канал", url=settings.channel.url),
        SimpleObject(title="Я подписался", style="success", callback="is_subscribed")
    ]
    return get_inline_keyboard(buttons_data, row_width=1)
