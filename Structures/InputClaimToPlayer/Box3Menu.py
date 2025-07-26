from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

from aiogram import Router

from Filters.PrivateChatFilter import PrivateChatFilter
from Structures.MenuNavigator import OutputInputFormMenu
from Filters.StatusFilter import StatusFilter


router = Router()


@router.message(StatusFilter(33), F.text.contains("Назад"))
async def ButtonBack(message: Message):
    
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 3)
    await OutputInputFormMenu(message)


@router.message(StatusFilter(33), F.text)
async def ButtonBack(message: Message):
    
    from SQLite.UpdateValues import UpdateValue, UpdateBoxValue
    UpdateBoxValue(message.from_user.id, "box3", message.text)
    UpdateValue(message.from_user.id, "users", "status", 3)
    await OutputInputFormMenu(message)


async def OutputBox3Menu(message: Message):
    kb = [
        [KeyboardButton(text="Гриферство")],
        [KeyboardButton(text="Читы")],
        [KeyboardButton(text="Чат")],
        [KeyboardButton(text="PvP")],
        [KeyboardButton(text="Дюп")],
        [KeyboardButton(text="VPN")],
        [KeyboardButton(text="Лагающие структуры")],
        [KeyboardButton(text="◀ [Назад]")]
    ]
    placeholder = "Введите текст:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("<b>[Ввод типа нарушения]</b>:", reply_markup=Keys)