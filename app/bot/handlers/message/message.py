from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.lexicon import LEXICON
from app.bot.states import Registration
from app.bot.handlers.utils import show_self_profile
from app.database.models import User


router = Router()


# @router.message(F.text == LEXICON.button.save_profile)
# async def save_profile_handler(message: Message, state: FSMContext,
#                                user: User, session: AsyncSession):
#     profile_data = await state.get_value("profile_data")
#     await save_profile(session, profile_data, user)
#     await message.answer("Успешно сохранено!")


# @router.message(F.text == LEXICON.button.my_profile)
# async def my_profile(message: Message, state: FSMContext, user: User):
#     pass
