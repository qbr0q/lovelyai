from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models import Ticket
from app.database.enums import TicketStatus
from app.support_bot.handlers.message.utils import search_ticket_id


router = Router()


@router.message(F.reply_to_message.from_user.is_bot)
async def reply_ticket(message: Message, session: AsyncSession):
    ticket: Ticket | None = None
    ticket_id = search_ticket_id(message.reply_to_message.text)
    if ticket_id:
        statement = (
            select(Ticket)
            .where(Ticket.id == ticket_id)
            .options(selectinload(Ticket.user))
        )
        result = await session.execute(statement)
        ticket = result.scalar_one_or_none()
    if ticket:
        await message.bot.send_message(
            chat_id=ticket.user.telegram_id,
            reply_to_message_id=ticket.message_id,
            text=f"Ответ по твоему обращению #{ticket_id}\n\n"
                 f"{message.text}\n"
                 f"С уважением, LuvlyAI. Если остались вопросы, можешь создать новый тикет."
        )
        ticket.status = TicketStatus.closed
