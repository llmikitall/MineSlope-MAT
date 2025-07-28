from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

from aiogram import Router

from Structures.TextVerification import TextVerification
from Structures.MenuNavigator import OutputInputFormMenu
from Filters.StatusFilter import StatusFilter


router = Router()


@router.message(StatusFilter(31), F.text.contains("Назад"))
async def ButtonBack(message: Message):
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 3)
    await OutputInputFormMenu(message)


@router.message(StatusFilter(31), F.text)
async def ButtonBack(message: Message):
    from SQLite.UpdateValues import UpdateValue, UpdateBoxValue
    text = await TextVerification(message.text)
    UpdateBoxValue(message.from_user.id, "box1", text)
    UpdateValue(message.from_user.id, "users", "status", 3)
    await OutputInputFormMenu(message)


async def OutputBox1Menu(message: Message):
    kb = [
        [KeyboardButton(text="◀ [Назад]")]
    ]
    placeholder = "Введите ник:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("<b>[Введите Ваш ник]</b>:", reply_markup=Keys)