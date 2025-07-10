from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

from aiogram import Router

from Middlewares.PrivateChatMiddleware import PrivateChatMiddleware
from StatusFilter import StatusFilter


router = Router()
router.message.middleware(PrivateChatMiddleware())


@router.message(F.text.contains("Назад"), StatusFilter(2))
async def ButtonBack(message: Message):
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 1)
    from Structures.MainMenu import OutputMainMenu
    await OutputMainMenu(message)


@router.message(F.text.contains("Создать"), StatusFilter(2))
async def ButtonCreate(message: Message):
    from SQLite.InsertValues import InsertValues
    await InsertValues("requests", (message.from_user.id, "4", "-", "-", "-", "-", "-", "-"))
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 3)
    from SQLite.SelectValues import FindMaxRequest
    UpdateValue(message.from_user.id, "users", "request", str(FindMaxRequest(message.from_user.id)))
    from Structures.InputFormMenu import OutputInputFormMenu
    await OutputInputFormMenu(message)


@router.message(F.text.contains("Запрос №"), StatusFilter(2))
async def ButtonRequest(message: Message):
    ID = message.text.split("№")
    from SQLite.SelectValues import SelectRequestsUser
    listing = SelectRequestsUser(message.from_user.id)
    if not ID[1].isdigit() or int(ID[1]) > len(listing):
        await message.answer("<b>[Эй! Ничего не знаю!]</b>:")
        return
    from SQLite.SelectValues import FindExitsRow

    if await FindExitsRow("requests", "ID", int(ID[1])) == 0:
        await message.answer("<b>[Такой запрос не найден...]</b>:")
        return
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 3)
    UpdateValue(message.from_user.id, "users", "request", int(ID[1]))
    from Structures.InputFormMenu import OutputInputFormMenu
    await OutputInputFormMenu(message)


async def OutputClaimToPlayer(message: Message):

    kb = [[KeyboardButton(text="Создать новую жалобу")]]

    from SQLite.SelectValues import SelectRequestsUser
    listing = SelectRequestsUser(message.from_user.id)
    for i in range(len(listing)):
        kb.append([KeyboardButton(text=f"Запрос №{len(listing)-i}")])
    kb.append([KeyboardButton(text="Назад")])
    placeholder = "Выберите жалобу:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("<b>[Жалоба на игрока]</b>:", reply_markup=Keys)
