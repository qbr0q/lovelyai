from sqlalchemy import func, select
from datetime import datetime, timedelta

from app.database.utils import get_session
from app.database.models import AIRequestLog


class LimitToken(Exception):
    def __str__(self):
        return "Превышен лимит токенов"


async def log_request(**kwargs):
    async with get_session() as session:
        log_record = AIRequestLog(**kwargs)
        session.add(log_record)
        await session.commit()


async def has_limit(token_limit, user_id):
    last_24_hours = datetime.utcnow() - timedelta(days=1)

    statement = (
        select(func.sum(AIRequestLog.tokens_used))
        .where(AIRequestLog.user_id == user_id)
        .where(AIRequestLog.created_at >= last_24_hours)
    )

    async with get_session() as session:
        result = await session.execute(statement)
        total_used = result.scalar() or 0

    return total_used > token_limit
