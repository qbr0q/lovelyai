from aiogram import Router
from aiogram.types import Message
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core import settings
from app.support_bot.handlers.states import Registration
from app.support_bot.handlers.registration.utils import generate_title
from app.database.models import User, Ticket
from app.database.enums import TicketStatus


router = Router()


@router.message(Registration.waiting_ticket)
async def waiting_ticket(message: Message,
                         user: User, session: AsyncSession):
    if len(message.text) <= 20:
        await message.answer("Слишком коротко\n"
                             "Опиши проблему подробнее (минимум 20 символов), иначе мы не сможем помочь")
    record = Ticket(
        title=generate_title(message.text),
        status=TicketStatus.open,
        text=message.text,
        message_id=message.message_id,
        user_id=user.id
    )
    session.add(record)
    await session.flush()

    await message.bot.send_message(chat_id=settings.social.staff_channel_id,
                                   text=f"📩 НОВЫЙ ТИКЕТ [#{record.id}]\n\n{message.text}")
    await message.answer(f"Получили твой запрос и уже разбираемся✨\n"
                         f"Номер обращения: {record.id}")
