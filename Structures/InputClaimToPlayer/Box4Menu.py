from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

from aiogram import Router

from Structures.MenuNavigator import OutputInputFormMenu
from Filters.StatusFilter import StatusFilter
from Structures.TextVerification import TextVerification

router = Router()


@router.message(StatusFilter(34), F.text.contains("Назад"))
async def ButtonBack(message: Message):
    
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 3)
    await OutputInputFormMenu(message)


@router.message(StatusFilter(34), F.text)
async def ButtonBack(message: Message):
    
    from SQLite.UpdateValues import UpdateValue, UpdateBoxValue
    text = await TextVerification(message.text)
    UpdateBoxValue(message.from_user.id, "box4", text)
    UpdateValue(message.from_user.id, "users", "status", 3)
    await OutputInputFormMenu(message)


async def OutputBox4Menu(message: Message):
    kb = [
        [KeyboardButton(text="◀ [Назад]")]
    ]
    placeholder = "Введите координаты:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("<b>[Введите координаты нарушения]</b>:\nПример: <i>«x:12 y:44 z:33»</i>",
                         reply_markup=Keys)
