from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

from aiogram import Router

from Filters.PrivateChatFilter import PrivateChatFilter
from Filters.StatusFilter import StatusFilter
from Structures.MenuNavigator import OutputInputFormMenu
from Structures.TextVerification import TextVerification

router = Router()


@router.message(StatusFilter(32), F.text.contains("Назад"))
async def ButtonBack(message: Message):
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 3)
    await OutputInputFormMenu(message)


@router.message(StatusFilter(32), F.text)
async def ButtonBack(message: Message):
    from SQLite.UpdateValues import UpdateValue, UpdateBoxValue
    text = await TextVerification(message.text)
    UpdateBoxValue(message.from_user.id, "box2", text)
    UpdateValue(message.from_user.id, "users", "status", 3)
    await OutputInputFormMenu(message)


async def OutputBox2Menu(message: Message):
    kb = [
        [KeyboardButton(text="◀ [Назад]")]
    ]
    placeholder = "Введите ник:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("<b>[Введите ник нарушителя]</b>:", reply_markup=Keys)
