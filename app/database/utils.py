from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.engine import SessionLocal


@asynccontextmanager
async def get_session():
    """
    Контекстный менеджер сессии: открывает, отдает и гарантированно закрывает.
    """
    session: AsyncSession = SessionLocal()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


async def get_session_dependency():
    """
    Генератор сессии: открывает, отдает и гарантированно закрывает.
    """
    session: AsyncSession = SessionLocal()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
