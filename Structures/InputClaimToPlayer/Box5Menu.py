import os

from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

from aiogram import Router

from Filters.PrivateChatFilter import PrivateChatFilter
from SQLite.SelectValues import SelectValues
from SQLite.UpdateValues import UpdateBoxValue, UpdateValue, UpdateValues
from Structures.MenuNavigator import OutputInputFormMenu
from Filters.StatusFilter import StatusFilter


router = Router()


@router.message(StatusFilter(35), F.text.contains("Назад"))
async def ButtonBack(message: Message):
    
    UpdateValue(message.from_user.id, "users", "status", 3)
    await OutputInputFormMenu(message)


@router.message(StatusFilter(35), F.text.contains("Удалить"))
async def ButtonBack(message: Message):
    ID = await SelectValues("request", "users", "userID = (?)", [message.from_user.id])
    await UpdateValues("requests", "box5 = '-'", "ID = (?)", [int(ID[0][0])])
    UpdateValue(message.from_user.id, "users", "status", 3)
    await OutputInputFormMenu(message)


@router.message(StatusFilter(35), F.photo)
async def PhotoDownloader(message: Message):
    DOWNLOAD_FOLDER = "Files/Photos/"
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    file_path = file.file_path

    file_name = f"file_{message.from_user.id}.{photo.file_id}.jpg"
    save_path = os.path.join(DOWNLOAD_FOLDER, file_name)

    ID = await SelectValues("request", "users", "userID = (?)", [message.from_user.id])
    listing = await SelectValues("box5", "requests", "ID = (?)",
                                 [int(ID[0][0])])
    if listing[0][0] == "-":
        UpdateBoxValue(message.from_user.id, "box5", save_path)
    else:
        UpdateBoxValue(message.from_user.id, "box5", f"{listing[0][0]}\n{save_path}")
    await message.bot.download_file(file_path, save_path)

    await OutputBox5Menu(message)


@router.message(StatusFilter(35))
async def ButtonBack(message: Message):
    await message.answer("<b>[Принимаются только фотографии!]</b>")


async def OutputBox5Menu(message: Message):
    ID = await SelectValues("request", "users", "userID = (?)", [message.from_user.id])
    box5 = await SelectValues("box5", "requests", "ID = (?)", [int(ID[0][0])])

    kb = []
    if box5[0][0] != "-":
        kb.append([KeyboardButton(text="🗑️ [Удалить все фото]")])
    kb.append([KeyboardButton(text="◀ [Назад]")])

    placeholder = "Вставьте фото:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("<b>[Вставьте фото]</b>:\nМожно загрузить сразу несколько фото.", reply_markup=Keys)
