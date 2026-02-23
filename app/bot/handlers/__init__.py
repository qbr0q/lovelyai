from app.bot.handlers.command import router as command_router
from app.bot.handlers.message import router as message_router
from app.bot.handlers.callback import router as callback_router
from app.bot.handlers.registration.registration import router as registration_router


routers = [command_router, message_router, callback_router, registration_router]
