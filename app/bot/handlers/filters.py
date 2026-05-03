from aiogram.filters import BaseFilter
from aiogram.types import Message

from app.database.models import User
from app.database.enums import UserRole


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message, user: User) -> bool:
        return user.role == UserRole.admin
