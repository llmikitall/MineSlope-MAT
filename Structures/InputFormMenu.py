from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

from aiogram import Router

from Middlewares.PrivateChatMiddleware import PrivateChatMiddleware
from StatusFilter import StatusFilter


router = Router()
router.message.middleware(PrivateChatMiddleware())


@router.message(F.text.contains("Назад"), StatusFilter(3))
async def ButtonBack(message: Message):
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "request", "-")
    UpdateValue(message.from_user.id, "users", "status", 2)
    from Structures.ClaimToPlayerMenu import OutputClaimToPlayer
    await OutputClaimToPlayer(message)


@router.message(F.text.contains("Ваш ник:"), StatusFilter(3))
async def ButtonBack(message: Message):
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 31)
    from Structures.Box1Menu import OutputBox1Menu
    await OutputBox1Menu(message)


@router.message(F.text.contains("Нарушитель"), StatusFilter(3))
async def ButtonBack(message: Message):
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 32)
    from Structures.Box2Menu import OutputBox2Menu
    await OutputBox2Menu(message)


@router.message(F.text.contains("Тип нарушения"), StatusFilter(3))
async def ButtonBack(message: Message):
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 33)
    from Structures.Box3Menu import OutputBox3Menu
    await OutputBox3Menu(message)


@router.message(F.text.contains("Координаты"), StatusFilter(3))
async def ButtonBack(message: Message):
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 34)
    from Structures.Box4Menu import OutputBox4Menu
    await OutputBox4Menu(message)


@router.message(F.text.contains("Доказательства"), StatusFilter(3))
async def ButtonBack(message: Message):
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 35)
    from Structures.Box5Menu import OutputBox5Menu
    await OutputBox5Menu(message)


@router.message(F.text.contains("Подробности"), StatusFilter(3))
async def ButtonBack(message: Message):
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 36)
    from Structures.Box6Menu import OutputBox6Menu
    await OutputBox6Menu(message)


async def OutputInputFormMenu(message: Message):
    from SQLite.SelectValues import SelectBoxsRequest, FindAnyRowUsers
    boxs = SelectBoxsRequest(FindAnyRowUsers(message.from_user.id, "request"))
    kb = [
        [KeyboardButton(text=f"Ваш ник: {boxs[0]}")],
        [KeyboardButton(text=f"Нарушитель: {boxs[1]}")],
        [KeyboardButton(text=f"Тип нарушения: {boxs[2]}")],
        [KeyboardButton(text=f"Координаты: {boxs[3]}")],
        [KeyboardButton(text=f"Доказательства: {boxs[4]}")],
        [KeyboardButton(text=f"Подробности: {boxs[5]}")],
        [KeyboardButton(text=f"Назад = Сохранить (пока что)")]
    ]
    placeholder = "Выберите жалобу:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("<b>[Жалоба на игрока]</b>:", reply_markup=Keys)
