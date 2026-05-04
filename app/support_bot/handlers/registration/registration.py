from aiogram import Router
from aiogram.types import Message

from app.core import settings
from app.support_bot.handlers.states import Registration


router = Router()


@router.message(Registration.waiting_ticket)
async def waiting_ticket(message: Message):
    await message.bot.send_message(chat_id=settings.social.staff_channel_id,
                                   text=f"📩 НОВЫЙ ТИКЕТ [#4435435]\n\n{message.text}")
    await message.answer("Получили твой запрос и уже разбираемся✨\n"
                         "Номер обращения: 4435435")
