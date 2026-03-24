from sqlmodel import select, and_
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.models import User
from app.core.constants import UserStatus
from .utils import MatchProfile


class MatchingService:
    async def get_match(self, current_user: User, session: AsyncSession):
        distance_col = User.bio_vector.cosine_distance(
            current_user.bio_vector
        ).label("dist")

        base_statement = select(
            User, distance_col
        ).filter(and_(
            User.status == UserStatus.active,
            User.deleted == False,
            User.id != current_user.id
        )).order_by(
            distance_col.asc()
        ).options(
            selectinload(User.media)
        )
        statement = self._set_filter(base_statement, current_user.filter)

        result = await session.exec(statement)
        profiles = self.prepare_profiles(
            result.all()
        )
        return profiles

    @staticmethod
    def _set_filter(statement, user_filter):
        if user_filter.target_gender:
            statement = statement.where(User.gender == user_filter.target_gender)
        if user_filter.min_age:
            statement = statement.where(User.age >= user_filter.min_age)
        if user_filter.max_age:
            statement = statement.where(User.age <= user_filter.max_age)
        if user_filter.target_city:
            statement = statement.where(User.gar_city == user_filter.target_city)

        return statement

    def prepare_profiles(self, records):
        result = []
        for record in records:
            user, dist = record
            match_profile = self._prepare_profile(user, dist)
            result.append(match_profile)
        return result

    @staticmethod
    def _prepare_profile(user, dist):
        match_profile = MatchProfile(
            id=user.id,
            name=user.name,
            age=user.age,
            city=user.city,
            gar_city=user.gar_city,
            bio=user.bio,
            media=user.media,
            match_percent=f"{max(0, (1 - dist)) * 100:.0f}%"
        )
        return match_profile
