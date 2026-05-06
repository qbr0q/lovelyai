from app.support_bot.handlers.command import router as command_router
from app.support_bot.handlers.registration import router as registration_router
from app.support_bot.handlers.message import router as message_router

routers = [command_router, registration_router, message_router]
