from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models import Ticket
from app.support_bot.handlers.states import Registration

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Поддержка LuvlyAI 🛠\n\n"
                         "Опиши свою проблему или задай вопрос — мы ответим максимально быстро.\n"
                         "/new_ticket — создать новое обращение\n"
                         "/my_tickets — посмотреть статус своих тикетов")


@router.message(Command("new_ticket"))
async def new_ticket(message: Message, state: FSMContext):
    await message.answer("Опиши свою проблему или задай вопрос — мы ответим максимально быстро")
    await state.set_state(Registration.waiting_ticket)
