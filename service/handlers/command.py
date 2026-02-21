from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):

    await message.answer("тест старта")


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
