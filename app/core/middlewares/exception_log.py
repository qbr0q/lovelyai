import traceback
import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import ErrorEvent


class ErrorLoggingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[ErrorEvent, Dict[str, Any]], Awaitable[Any]],
            event: ErrorEvent,
            data: Dict[str, Any]
    ) -> Any:
        logging.error(f"user_profile.id={data.get('event_from_user').id}\n"
                      f"{traceback.format_exc(limit=-1)}")
        return
