from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from app.database.models import User


class UserRegistrationMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        session: AsyncSession = data["session"]
        telegram_id = event.event.from_user.id

        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()

        data["user"] = user

        return await handler(event, data)
