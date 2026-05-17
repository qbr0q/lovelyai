from taskiq import TaskiqDepends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.task_schedule import broker, bot
from app.database.utils import get_session_dependency
from app.database.models import User


@broker.task(schedule=[{"cron": "07 22 * * *"}])
async def test(
    session: AsyncSession = TaskiqDepends(get_session_dependency)
):
    statement = (
        select(User)
        .where(User.id == 1)
    )
    result = await session.execute(statement)
    user: User = result.scalar()
    await bot.send_message(user.telegram_id, "test")


# @broker.task(schedule=[{"interval": "10"}])
# async def test():
#     print("test")
