from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.database.models import User
from app.support_bot.handlers.states import Registration

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Поддержка LuvlyAI 🛠\n\n"
                         "Опиши свою проблему или задай вопрос — мы ответим максимально быстро.\n"
                         "/new_ticket — создать новое обращение")


@router.message(Command("new_ticket"))
async def new_ticket(message: Message, state: FSMContext):
    await message.answer("Опиши свою проблему или задай вопрос — мы ответим максимально быстро")
    await state.set_state(Registration.waiting_ticket)


@router.message(Command("my_tickets"))
async def my_tickets(message: Message, user:  User):
    pass
