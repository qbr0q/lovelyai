from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from app.core import config
from app.bot.handlers import routers
from app.core.middlewares import DbSessionMiddleware, UserRegistrationMiddleware, \
    AlbumMiddleware, ErrorLoggingMiddleware
from app.common.utils import SimpleObject as so, get_proxy_session
from app.database import SessionLocal
from app.services import AIService, GARService, MatchingService


def include_routers(dp):
    for router in routers:
        dp.include_router(router)


def include_middleware(dp):
    dp.update.middleware(DbSessionMiddleware(session_pool=SessionLocal))
    dp.update.middleware(UserRegistrationMiddleware())
    dp.message.middleware(AlbumMiddleware())
    dp.errors.outer_middleware(ErrorLoggingMiddleware())


async def setup_app():
    session = get_proxy_session()
    bot = Bot(token=config.private.bot_token, session=session)
    storage = RedisStorage.from_url(config.redis.url)
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
