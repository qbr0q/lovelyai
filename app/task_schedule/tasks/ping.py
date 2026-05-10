from taskiq import TaskiqDepends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.task_schedule.main import broker
from app.database.utils import get_session_dependency
from app.database.models import User


@broker.task(schedule=[{"interval": "10"}])
async def my_periodic_task(
    session: AsyncSession = TaskiqDepends(get_session_dependency)
):
    statement = (
        select(User)
        .where(User.id == 1)
    )
    result = await session.execute(statement)
    print(result)
