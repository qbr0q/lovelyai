from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.handlers.command.utils import get_reply_keyboard
from app.core.lexicon import LEXICON


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    buttons = [LEXICON.button.create_profile, LEXICON.button.import_profile]
    reply_markup = get_reply_keyboard(buttons)

    await message.answer(LEXICON.start, reply_markup=reply_markup)


@router.message(Command("app"))
async def open_app(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Открыть LuvlyAI",
        web_app=WebAppInfo(url="https://google.com")
    )

    await message.answer(
        "Нажми на кнопку, чтобы открыть приложение:",
        reply_markup=builder.as_markup()
    )
