from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

from aiogram import Router
from Structures.MenuNavigator import OutputInputFormMenu
from Filters.StatusFilter import StatusFilter
from SQLite.UpdateValues import UpdateValue

router = Router()


@router.message(F.text.contains("Назад"), StatusFilter(36))
async def ButtonBack(message: Message):
    UpdateValue(message.from_user.id, "users", "status", 3)
    await OutputInputFormMenu(message)


@router.message(F.text, StatusFilter(36))
async def ButtonBack(message: Message):
    from SQLite.UpdateValues import UpdateBoxValue
    UpdateBoxValue(message.from_user.id, "box6", message.text)
    UpdateValue(message.from_user.id, "users", "status", 3)
    await OutputInputFormMenu(message)


@router.message(StatusFilter(36))
async def ButtonBack(message: Message):
    await message.answer("Не пойму... ты мне что пытаешься скинуть..?")


async def OutputBox6Menu(message: Message):
    kb = [
        [KeyboardButton(text="Назад")]
    ]
    placeholder = "Введите текст:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("<b>[Ввод подробностей]</b>:", reply_markup=Keys)