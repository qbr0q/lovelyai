from app.core import config

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession


db = config.db

db_url = f"postgresql+asyncpg://{db.user}:{db.password}@{db.host}:{db.port}/{db.db}"

engine = create_async_engine(db_url)
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
