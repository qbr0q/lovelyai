import asyncio
from aiogram import Bot, Dispatcher
from service.core import start_bot
from service.core.config import config


bot = Bot(token=config.bot_token)
dp = Dispatcher()


async def main():
    await start_bot(bot, dp)


if __name__ == "__main__":
    asyncio.run(main())
