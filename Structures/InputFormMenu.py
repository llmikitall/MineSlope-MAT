from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram import F, Bot

from aiogram import Router
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Filters.StatusFilter import StatusFilter
from Structures.MenuNavigator import (OutputClaimToPlayerMenu, OutputBox1Menu, OutputBox2Menu, OutputBox3Menu,
                                      OutputBox4Menu, OutputBox5Menu, OutputBox6Menu, OutputMainMenu)
from SQLite.UpdateValues import UpdateValue
from SQLite.UpdateValues import UpdateValues
from SQLite.SelectValues import SelectValues
from Structures.Box1Menu import router as box1_router
from Structures.Box2Menu import router as box2_router
from Structures.Box3Menu import router as box3_router
from Structures.Box4Menu import router as box4_router
from Structures.Box5Menu import router as box5_router
from Structures.Box6Menu import router as box6_router

router = Router()
router.include_routers(box1_router, box2_router, box3_router, box4_router, box5_router, box6_router)


@router.message(StatusFilter(3), F.text.contains("Назад"))
async def ButtonBack(message: Message):
    userID = message.from_user.id
    request = await SelectValues("request", "users", "userID = (?);", [userID])
    status = await SelectValues("status", "requests", "ID = (?) AND userID = (?);", [int(request[0][0]), str(userID)])
    if status[0][0] == "creating":
        await UpdateValues("requests", "status = 'delete'", "ID = (?) AND userID = (?)",
                           [int(request[0][0]), str(userID)])
    UpdateValue(message.from_user.id, "users", "request", "-")
    UpdateValue(message.from_user.id, "users", "status", 2)
    await OutputClaimToPlayerMenu(message)


@router.message(StatusFilter(3), F.text.contains("Сохранить"))
async def ButtonBack(message: Message, bot: Bot):
    userID = message.from_user.id
    request = await SelectValues("request", "users", "userID = (?);", [userID])
    status = await SelectValues("status", "requests", "ID = (?) AND userID = (?);", [int(request[0][0]), str(userID)])
    if status[0][0] == "creating":

        listing = await SelectValues("*", "requests", "ID = (?) AND userID = (?)", [int(request[0][0]), str(userID)])

        user_name = message.from_user.full_name
        user_link = (
            f"<a href='https://t.me/{message.from_user.username}'>{user_name}</a>"
            if message.from_user.username
            else user_name
        )

        text = (f"<b>Запрос №{listing[0][0]:03d}:</b> ⚙\n"
                f"--------------------------------\n"
                f"  <b>1) Ник игрока:</b> {listing[0][4]}\n"
                f"  <b>2) Ник нарушителя:</b> {listing[0][5]}\n"
                f"  <b>3) Тип нарушения:</b> {listing[0][6]}\n"
                f"  <b>4) Координаты:</b> {listing[0][7]}\n"
                f"  <b>5) Подробности:</b> {listing[0][9]}\n"
                f"  <b>6) Доказательства:</b> [---]\n"
                f"--------------------------------\n"
                f"✍️ <b>Написано</b>: {user_link}\n"
                f"--------------------------------\n")
        await UpdateValues("requests", "status = 'await', htmlText = (?)", "ID = (?) AND userID = (?)",
                           [text, int(request[0][0]), str(userID)])
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(
            text="⚙ Действия",
            callback_data="actions"
        ))
        await message.bot.send_message(chat_id=-1002691896200, message_thread_id=4, reply_markup=keyboard.as_markup(),
                                       text=text)
    UpdateValue(message.from_user.id, "users", "request", "-")
    UpdateValue(message.from_user.id, "users", "status", 1)
    await OutputMainMenu(message)


@router.message(StatusFilter(3), F.text.contains("Ваш ник:"))
async def ButtonBack(message: Message):
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 31)
    await OutputBox1Menu(message)


@router.message(StatusFilter(3), F.text.contains("Нарушитель"))
async def ButtonBack(message: Message):
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 32)
    await OutputBox2Menu(message)


@router.message(StatusFilter(3), F.text.contains("Тип нарушения"))
async def ButtonBack(message: Message):
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 33)
    await OutputBox3Menu(message)


@router.message(StatusFilter(3), F.text.contains("Координаты"))
async def ButtonBack(message: Message):
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 34)
    await OutputBox4Menu(message)


@router.message(StatusFilter(3), F.text.contains("Доказательства"))
async def ButtonBack(message: Message):
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 35)
    await OutputBox5Menu(message)


@router.message(StatusFilter(3), F.text.contains("Подробности"))
async def ButtonBack(message: Message):
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 36)
    await OutputBox6Menu(message)


async def OutputInputFormMenu(message: Message):
    from SQLite.SelectValues import SelectBoxsRequest, FindAnyRowUsers
    boxs = SelectBoxsRequest(FindAnyRowUsers(message.from_user.id, "request"))
    kb = [
        [KeyboardButton(text=f"Ваш ник: {boxs[0]}")],
        [KeyboardButton(text=f"Нарушитель: {boxs[1]}")],
        [KeyboardButton(text=f"Тип нарушения: {boxs[2]}")],
        [KeyboardButton(text=f"Координаты: {boxs[3]}")],
        [KeyboardButton(text=f"Доказательства: {boxs[4]}")],
        [KeyboardButton(text=f"Подробности: {boxs[5]}")],
        [KeyboardButton(text=f"Сохранить")],
        [KeyboardButton(text=f"Назад")]
    ]
    placeholder = "Выберите жалобу:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("<b>[Жалоба на игрока]</b>:", reply_markup=Keys)



