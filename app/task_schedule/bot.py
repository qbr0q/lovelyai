from aiogram import Bot

from app.core import config
from app.common.utils import get_proxy_session


session = get_proxy_session()
bot = Bot(token=config.private.bot_token, session=session)
