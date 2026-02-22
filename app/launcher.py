from aiogram import Bot, Dispatcher
from app.services.ai_service import AIService
from aiogram.fsm.storage.memory import MemoryStorage
from app.core import config
from app.bot.handlers import routers
from types import SimpleNamespace as sn


def include_routers(dp):
    for router in routers:
        dp.include_router(router)


async def setup_app():
    bot = Bot(token=config.bot_token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    ai_service = AIService()

    include_routers(dp)

    return sn(
        bot=bot,
        dp=dp,
        ai_service=ai_service
    )


async def start_app():
    app_components = await setup_app()

    dp = app_components.dp
    bot = app_components.bot

    await dp.start_polling(
        bot,
        ai_service=app_components.ai_service
    )
