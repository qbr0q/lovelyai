from app.database.models import User, UserFilter
from app.core.constants import UserStatus


async def save_user(session, profile_data, telegram_id):
    user_record = User(
        telegram_id=telegram_id,
        gender=profile_data.gender,
        name=profile_data.name,
        age=int(profile_data.age),
        city=profile_data.city,
        bio=profile_data.bio,
        status=UserStatus.active
    )
    session.add(user_record)
    await session.flush()

    user_filter_record = UserFilter(user_id=user_record.id)
    session.add(user_filter_record)
