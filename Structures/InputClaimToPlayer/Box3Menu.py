from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

from aiogram import Router

from Filters.PrivateChatFilter import PrivateChatFilter
from Structures.MenuNavigator import OutputInputFormMenu
from Filters.StatusFilter import StatusFilter
from Structures.TextVerification import TextVerification

router = Router()


@router.message(StatusFilter(33), F.text.contains("Назад"))
async def ButtonBack(message: Message):
    
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 3)
    await OutputInputFormMenu(message)


@router.message(StatusFilter(33), F.text)
async def ButtonBack(message: Message):

    from SQLite.UpdateValues import UpdateValue, UpdateBoxValue
    text = await TextVerification(message.text)
    UpdateBoxValue(message.from_user.id, "box3", text)
    UpdateValue(message.from_user.id, "users", "status", 3)
    await OutputInputFormMenu(message)


async def OutputBox3Menu(message: Message):
    kb = [
        [KeyboardButton(text="🖕 [Гриферство]")],
        [KeyboardButton(text="🎮 [Читы]")],
        [KeyboardButton(text="💬 [Чат]")],
        [KeyboardButton(text="⚔️ [PvP]")],
        [KeyboardButton(text="♻️ [Дюп]")],
        [KeyboardButton(text="🌐 [VPN]")],
        [KeyboardButton(text="🏗️ [Лаг. структуры]")],
        [KeyboardButton(text="◀ [Назад]")]
    ]
    placeholder = "Выберите тип:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("<b>[Укажите тип нарушения]</b>:", reply_markup=Keys)