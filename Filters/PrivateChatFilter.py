from aiogram.filters import BaseFilter
from aiogram.types import Message
from SQLite.SelectValues import FindAnyRowUsers


# StatusFilter - фильтр статуса для router.message(...). В init передаётся (статус №1), с которым допускается
# пользователь. В call сравнение (статуса №1) с текущим статусом пользователя. Если статусы равны - пользователю
# дозволяется выполнить метод. Иначе - пропускает этот метод.


class PrivateChatFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.chat.type == "private":
            return True
        else:
            return False
