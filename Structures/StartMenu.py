from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Router

from Middlewares.PrivateChatMiddleware import PrivateChatMiddleware

router = Router()
router.message.middleware(PrivateChatMiddleware())


@router.message(CommandStart())
async def CommandStart(message: Message):
    from SQLite.SelectValues import FindExitsRow
    if await FindExitsRow("users", "userID", message.from_user.id) == 0:
        from SQLite.InsertValues import InsertValues
        await InsertValues("users", [message.from_user.id])
    from Structures.MainMenu import OutputMainMenu
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 1)
    await OutputMainMenu(message)
