import os.path

from aiogram import Router, F
from aiogram.types import Message

from Middlewares.PrivateChatMiddleware import PrivateChatMiddleware

router = Router()
router.message.middleware(PrivateChatMiddleware())


@router.message(F.photo)
async def BadPhoto(message: Message):
    DOWNLOAD_FOLDER = "Files"
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    file_path = file.file_path

    file_name = f"file_{message.from_user.id}.jpg"
    save_path = os.path.join(DOWNLOAD_FOLDER, file_name)
    await message.bot.download_file(file_path, save_path)


@router.message()
async def BadMessage(message: Message):
    # await message.bot.send_message("-1002691896200", message.text, message_thread_id=4)
    print(message.from_user.id)
    await message.answer("<b>Не пойму...</b> что ты вводишь?")
    await message.answer_sticker("CAACAgIAAxkBAAEHoX1mucVzt3Z7abLiXoLUUS6Rf2lxNgACEAADwDZPE-qBiinxHwLoNQQ")
