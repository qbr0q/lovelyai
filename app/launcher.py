from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.core import config
from app.core.middlewares import DbSessionMiddleware, UserRegistrationMiddleware, AlbumMiddleware
from app.core.utils import SimpleObject as so
from app.database import async_session_factory, init_db
from app.bot.handlers import routers
from app.services import AIService, GARService


def include_routers(dp):
    for router in routers:
        dp.include_router(router)


def include_middleware(dp):
    dp.update.middleware(DbSessionMiddleware(session_pool=async_session_factory))
    dp.update.middleware(UserRegistrationMiddleware())
    dp.message.middleware(AlbumMiddleware())


async def setup_app():
    bot = Bot(token=config.bot_token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    ai_service = AIService()
    gar_service = GARService()

    include_routers(dp)
    include_middleware(dp)

    await init_db()

    return so(
        bot=bot,
        dp=dp,
        ai_service=ai_service,
        gar_service=gar_service
    )


async def start_app():
    app_components = await setup_app()

    dp = app_components.dp
    bot = app_components.bot

    await dp.start_polling(
        bot,
        ai_service=app_components.ai_service,
        gar_service=app_components.gar_service
    )
