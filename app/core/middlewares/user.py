from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update, User as TgUser
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database.models import User


class UserRegistrationMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:
        tg_user: TgUser = data.get("event_from_user")
        session: AsyncSession = data["session"]
        telegram_id = tg_user.id

        statement = (
            select(User)
            .where(User.telegram_id == telegram_id)
            .options(
                selectinload(User.media),
                selectinload(User.filter)
            )
        )
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        data["user"] = user

        return await handler(event, data)
