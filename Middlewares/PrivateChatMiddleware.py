from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message


# Милдварь . Будет проверять, а является ли пользователь злоумышленником?
class PrivateChatMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        if event.chat.type != "private":
            return
        print(f"[{event.from_user.id}] {event.text}")
        return await handler(event, data)