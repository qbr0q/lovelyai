from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from app.core import config
from app.support_bot.handlers import routers
from app.core.middlewares import DbSessionMiddleware, UserRegistrationMiddleware, \
    ErrorLoggingMiddleware
from app.common.utils import SimpleObject as so, get_proxy_session
from app.database import SessionLocal


def include_routers(dp):
    for router in routers:
        dp.include_router(router)


def include_middleware(dp):
    dp.update.middleware(DbSessionMiddleware(session_pool=SessionLocal))
    dp.update.middleware(UserRegistrationMiddleware())
    # dp.message.middleware(AlbumMiddleware())
    dp.errors.outer_middleware(ErrorLoggingMiddleware())


async def setup_app():
    session = get_proxy_session()
    bot = Bot(token=config.private.support_bot_token, session=session)
    storage = RedisStorage.from_url(config.redis.url)
    dp = Dispatcher(storage=storage)

    include_routers(dp)
    include_middleware(dp)

    return so(
        bot=bot,
        dp=dp
    )


async def start_app():
    app_components = await setup_app()

    dp = app_components.dp
    bot = app_components.bot

    await dp.start_polling(
        bot
    )
