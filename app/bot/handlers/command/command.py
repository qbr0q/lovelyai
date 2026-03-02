from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.handlers.utils import get_start_rm
from app.core.lexicon import LEXICON


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    rm = get_start_rm()

    await message.answer(LEXICON.start, reply_markup=rm)


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
