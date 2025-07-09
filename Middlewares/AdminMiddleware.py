from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message


class AdminMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        if event.from_user.id != 6609070015 and event.from_user.id != 919436925:
            return

        return await handler(event, data)
