from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession

from app.core import config, settings
from app.bot.handlers import routers
from app.bot.middlewares import DbSessionMiddleware, UserRegistrationMiddleware, AlbumMiddleware
from app.core.utils import SimpleObject as so
from app.database import SessionLocal
from app.services import AIService, GARService, MatchingService


def include_routers(dp):
    for router in routers:
        dp.include_router(router)


def include_middleware(dp):
    dp.update.middleware(DbSessionMiddleware(session_pool=SessionLocal))
    dp.update.middleware(UserRegistrationMiddleware())
    dp.message.middleware(AlbumMiddleware())


def get_proxy_session():
    session = None
    if settings.use_proxy:
        session = AiohttpSession(proxy=config.proxy.url)
    return session


async def setup_app():
    session = get_proxy_session()
    bot = Bot(token=config.bot_token, session=session)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    ai_service = AIService()
    gar_service = GARService()
    match_service = MatchingService()

    include_routers(dp)
    include_middleware(dp)

    return so(
        bot=bot,
        dp=dp,
        ai_service=ai_service,
        gar_service=gar_service,
        match_service=match_service
    )


async def start_app():
    app_components = await setup_app()

    dp = app_components.dp
    bot = app_components.bot

    await dp.start_polling(
        bot,
        ai_service=app_components.ai_service,
        gar_service=app_components.gar_service,
        match_service=app_components.match_service
    )
