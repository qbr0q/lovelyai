from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core import LEXICON
from app.bot.states import Registration
from app.database.models import User
from app.bot.handlers.utils import show_self_profile
from .utils import create_user


router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext,
                user: User, session: AsyncSession):
    if not user:
        user = create_user(message.from_user)
        session.add(user)
    if user.is_empty:
        await state.set_state(Registration.waiting_self_profile)
        await message.answer(LEXICON.start)
    else:
        await show_self_profile(message, state, user)


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
