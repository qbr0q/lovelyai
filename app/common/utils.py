from typing import Optional, List
from pydantic import BaseModel
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession

from app.core import config, settings


class SimpleObject:
    def __init__(self, **kwargs):
        for i, v in kwargs.items():
            setattr(self, i, v)

    def __getattr__(self, item):
        return self.__dict__.get(item)


class Profile(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    city: Optional[str] = None
    gar_city: Optional[str] = None
    bio: Optional[str] = None
    bio_vector: Optional[List[float]] = None
    media: List[str] = []


async def notify_target_user(bot, target_id, msg, button_data=None):
    await bot.send_message(target_id, msg,
                           reply_markup=button_data, parse_mode=ParseMode.HTML)


def get_proxy_session():
    session = None
    if settings.use_proxy:
        session = AiohttpSession(proxy=config.proxy.url)
    return session
