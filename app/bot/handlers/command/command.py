from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from sqlmodel.ext.asyncio.session import AsyncSession

from app.bot.states import Registration
from app.core.lexicon import LEXICON
from app.database.models import User
from .utils import create_user


router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext,
                user: User, session: AsyncSession):
    if not user:
        create_user(session, message.from_user.id)
    await state.set_state(Registration.waiting_self_profile)

    await message.answer(LEXICON.start)


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
