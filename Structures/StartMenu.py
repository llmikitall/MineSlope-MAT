from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Router

from Middlewares.PrivateChatMiddleware import PrivateChatMiddleware

router = Router()
router.message.middleware(PrivateChatMiddleware())


@router.message(CommandStart())
async def CommandStart(message: Message):
    print(message.from_user.id)
    from Structures.MainMenu import OutputMainMenu
    await OutputMainMenu(message)
