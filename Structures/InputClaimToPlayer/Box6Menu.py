from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

from aiogram import Router

from Structures.MenuNavigator import OutputInputFormMenu
from Filters.StatusFilter import StatusFilter
from SQLite.UpdateValues import UpdateValue
from Structures.TextVerification import TextVerification

router = Router()


@router.message(StatusFilter(36), F.text.contains("Назад"))
async def ButtonBack(message: Message):
    
    UpdateValue(message.from_user.id, "users", "status", 3)
    await OutputInputFormMenu(message)


@router.message(StatusFilter(36), F.text)
async def ButtonBack(message: Message):
    text = await TextVerification(message.text)
    from SQLite.UpdateValues import UpdateBoxValue
    UpdateBoxValue(message.from_user.id, "box6", text)
    UpdateValue(message.from_user.id, "users", "status", 3)
    await OutputInputFormMenu(message)


async def OutputBox6Menu(message: Message):
    kb = [
        [KeyboardButton(text="◀ [Назад]")]
    ]
    placeholder = "Введите детали:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("<b>[Введите детали нарушения]</b>:", reply_markup=Keys)