from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

from aiogram import Router

from Middlewares.PrivateChatMiddleware import PrivateChatMiddleware
from StatusFilter import StatusFilter


router = Router()
router.message.middleware(PrivateChatMiddleware())


@router.message(F.text.contains("Назад"), StatusFilter(34))
async def ButtonBack(message: Message):
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 3)
    from Structures.InputFormMenu import OutputInputFormMenu
    await OutputInputFormMenu(message)


@router.message(F.text, StatusFilter(34))
async def ButtonBack(message: Message):
    from SQLite.UpdateValues import UpdateValue, UpdateBoxValue
    UpdateBoxValue(message.from_user.id, "box4", message.text)
    UpdateValue(message.from_user.id, "users", "status", 3)
    from Structures.InputFormMenu import OutputInputFormMenu
    await OutputInputFormMenu(message)


@router.message(StatusFilter(34))
async def ButtonBack(message: Message):
    await message.answer("Не пойму... ты мне что пытаешься скинуть..?")


async def OutputBox4Menu(message: Message):
    kb = [
        [KeyboardButton(text="Назад")]
    ]
    placeholder = "Введите текст:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("<b>[Ввод координат нарушения]</b>:", reply_markup=Keys)