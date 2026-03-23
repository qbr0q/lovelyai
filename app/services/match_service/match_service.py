from sqlmodel import select, and_

from app.database.models import User
from app.core.constants import UserStatus
from sqlmodel.ext.asyncio.session import AsyncSession


class MatchingService:
    async def get_match(self, user: User, session: AsyncSession):
        base_statement = select(
            User
        ).filter(and_(
            User.status == UserStatus.active,
            User.deleted == False,
            User.id != user.id
        ))
        statement = self._set_filter(base_statement, user.filter)

    @staticmethod
    def _set_filter(statement, user_filter):
        if user_filter.target_gender:
            statement = statement.where(User.gender == user_filter.target_gender)
        if user_filter.min_age:
            statement = statement.where(User.age >= user_filter.min_age)
        if user_filter.max_age:
            statement = statement.where(User.age <= user_filter.max_age)
        if user_filter.target_city:
            statement = statement.where(User.city == user_filter.target_city)

        return statement
