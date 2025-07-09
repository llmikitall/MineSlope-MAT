
from aiogram import Router
from aiogram.types import Message, ChatPermissions
from aiogram.filters import Command

from Middlewares.AdminMiddleware import AdminMiddleware

router = Router()
router.message.middleware(AdminMiddleware())


@router.message(Command("chat", prefix="/"))
async def chatID(message: Message):
    await message.answer(f"[+] ID чата: {message.chat.id}\n[+] ID темы: {message.message_thread_id}")
    thread_id = message.message_thread_id if message.is_topic_message else None
    await message.bot.send_message(message.chat.id, "Теперь я знаю о Вас БОЛЬШЕ!!", message_thread_id=thread_id)


