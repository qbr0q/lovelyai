from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlmodel.ext.asyncio.session import AsyncSession


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("test")
