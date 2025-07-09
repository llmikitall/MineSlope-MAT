
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from Middlewares.AdminMiddleware import AdminMiddleware

router = Router()
router.message.middleware(AdminMiddleware())


@router.message(Command("", prefix="!"))
async def HelpCommand(message: Message):
    text = """Список команд для Администратора:
    1) <b>[!Тема]</b> - в данный момент просто смотрит текущий ID чата и, если есть, ID топика.
    2) <b>[!Уничтожить <i>{Table}</i>]</b> - удаляет указанную таблицу. (Для разработчика)
    """
    await message.answer(text)


@router.message(Command("Тема", prefix="!"))
async def TopicCommand(message: Message):
    await message.answer(f"[+] ID чата: {message.chat.id}\n[+] ID темы: {message.message_thread_id}")
    # thread_id = message.message_thread_id if message.is_topic_message else None
    # await message.bot.send_message(message.chat.id, "Теперь я знаю о Вас БОЛЬШЕ!!", message_thread_id=thread_id)


@router.message(Command("Уничтожить", prefix="!"))
async def DropCommand(message: Message, command: CommandObject):
    userID = message.chat.id
    if userID != 6609070015:
        await message.answer("[-] Команда недоступна для Вас, для безопасности...")
        return
    if command.args is None:
        await message.answer("Команда введена неправильно: !Уничтожить {Table}")
        return
    from SQLite.DropTables import DropTable
    if command.args == "requests":
        await DropTable("requests")
        await message.answer("[+] Таблица <b>'request'</b> была удалена!")
    elif command.args == "users":
        await DropTable("users")
        await message.answer("[+] Таблица <b>'users'</b> была удалена!")
    else:
        await message.answer("[-] Хмм..? Не знаю я такой таблицы...")
