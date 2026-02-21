from service.handlers import routers


async def start_bot(bot, dp):
    include_routers(dp)

    await dp.start_polling(bot)


def include_routers(dp):
    for router in routers:
        dp.include_router(router)
