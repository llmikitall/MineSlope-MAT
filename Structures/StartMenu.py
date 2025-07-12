from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Router

from SQLite.SelectValues import FindExitsRow
from SQLite.InsertValues import InsertValues
from Structures.MainMenu import router as main_menu_router
from Structures.MenuNavigator import OutputMainMenu
from SQLite.UpdateValues import UpdateValue
from Filters.PrivateChatFilter import PrivateChatFilter

router = Router()
router.message.filter(PrivateChatFilter())
router.include_router(main_menu_router)


@router.message(CommandStart())
async def CommandStart(message: Message):
    # /start - инициализация пользователей и возврат в главное меню.
    userID = message.from_user.id

    # Проверка пользователя в базе данных
    if await FindExitsRow("users", "userID", userID) == 0:
        await InsertValues("users", "(userID)", "(?)", [str(userID)])

    # Обновление статуса для главного меню
    UpdateValue(userID, "users", "status", 1)
    await OutputMainMenu(message)
