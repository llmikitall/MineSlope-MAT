import os

from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, \
    FSInputFile
from aiogram import F

from aiogram import Router
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Filters.StatusFilter import StatusFilter
from Structures.MenuNavigator import (OutputClaimToPlayerMenu, OutputBox1Menu, OutputBox2Menu, OutputBox3Menu,
                                      OutputBox4Menu, OutputBox5Menu, OutputBox6Menu, OutputMainMenu)
from SQLite.UpdateValues import UpdateValue
from SQLite.UpdateValues import UpdateValues
from SQLite.SelectValues import SelectValues
from Structures.InputClaimToPlayer.Box1Menu import router as box1_router
from Structures.InputClaimToPlayer.Box2Menu import router as box2_router
from Structures.InputClaimToPlayer.Box3Menu import router as box3_router
from Structures.InputClaimToPlayer.Box4Menu import router as box4_router
from Structures.InputClaimToPlayer.Box5Menu import router as box5_router
from Structures.InputClaimToPlayer.Box6Menu import router as box6_router

router = Router()
router.include_routers(box1_router, box2_router, box3_router, box4_router, box5_router, box6_router)


# Удаление при creating и editing!
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
async def ButtonBack(message: Message):
    userID = message.from_user.id
    ID = await SelectValues("request", "users", "userID = (?)", [userID])
    boxs = await SelectValues("box1, box2, box3, box4, box5, box6",
                              "requests",
                              "ID = (?)",
                              [int(ID[0][0])])

    additionally = await SelectValues("status, editable",
                                      "requests",
                                      "ID = (?)",
                                      [int(ID[0][0])])
    if additionally[0][1] == 0:
        await message.answer("Ни-ни... Запрос уже обработан!")
        return

    if additionally[0][0] == "creating":
        check = ""
        if boxs[0][0] == "-":
            check += "  - <b>Ваш ник</b>;\n"
        if boxs[0][1] == "-":
            check += "  - <b>Ник нарушителя</b>;\n"
        if boxs[0][2] == "-":
            check += "  - <b>Тип нарушения</b>;\n"
        if check != "":
            await message.answer("[Укажите, пожалуйста, следующее]:\n" + check)
            return

        text = await PreviewText(message, ID, boxs)

        await UpdateValues("requests", "status = 'await', htmlText = (?)", "ID = (?)",
                           [text, int(ID[0][0])])
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(
            text="⚙ Действия",
            callback_data="actions"
        ))

        messageID = await message.bot.send_message(
            chat_id=-1002691896200,
            message_thread_id=4,
            text=text,
            reply_markup=keyboard.as_markup()
        )
        await UpdateValues("requests", "messageID = (?)", "ID = (?)", [messageID.message_id, int(ID[0][0])])

        # Список фото (локальные пути)
        if boxs[0][4] != "-":
            splitListing = boxs[0][4].split("\n")
            existing_photos = [path for path in splitListing if os.path.exists(path)]
            if existing_photos:
                media = [InputMediaPhoto(media=FSInputFile(path)) for path in existing_photos]
                await message.bot.send_media_group(
                    chat_id=-1002691896200,
                    message_thread_id=4,
                    media=media,
                    reply_to_message_id=messageID.message_id  # Привязка к тексту
                )

    UpdateValue(message.from_user.id, "users", "request", "-")
    UpdateValue(message.from_user.id, "users", "status", 1)
    await OutputMainMenu(message)


@router.message(StatusFilter(3), F.text.contains("Ваш ник"))
async def ButtonBack(message: Message):
    userID = message.from_user.id
    ID = await SelectValues("request", "users", "userID = (?)", [userID])
    additionally = await SelectValues("status, editable",
                                      "requests",
                                      "ID = (?)",
                                      [int(ID[0][0])])
    if additionally[0][1] == 0:
        await message.answer("Ни-ни... Запрос уже обработан!")
        return

    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 31)
    await OutputBox1Menu(message)


@router.message(StatusFilter(3), F.text.contains("Нарушитель"))
async def ButtonBack(message: Message):
    userID = message.from_user.id
    ID = await SelectValues("request", "users", "userID = (?)", [userID])
    additionally = await SelectValues("status, editable",
                                      "requests",
                                      "ID = (?)",
                                      [int(ID[0][0])])
    if additionally[0][1] == 0:
        await message.answer("Ни-ни... Запрос уже обработан!")
        return
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 32)
    await OutputBox2Menu(message)


@router.message(StatusFilter(3), F.text.contains("Тип нарушения"))
async def ButtonBack(message: Message):
    userID = message.from_user.id
    ID = await SelectValues("request", "users", "userID = (?)", [userID])
    additionally = await SelectValues("status, editable",
                                      "requests",
                                      "ID = (?)",
                                      [int(ID[0][0])])
    if additionally[0][1] == 0:
        await message.answer("Ни-ни... Запрос уже обработан!")
        return

    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 33)
    await OutputBox3Menu(message)


@router.message(StatusFilter(3), F.text.contains("Координаты"))
async def ButtonBack(message: Message):
    userID = message.from_user.id
    ID = await SelectValues("request", "users", "userID = (?)", [userID])
    additionally = await SelectValues("status, editable",
                                      "requests",
                                      "ID = (?)",
                                      [int(ID[0][0])])
    if additionally[0][1] == 0:
        await message.answer("Ни-ни... Запрос уже обработан!")
        return

    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 34)
    await OutputBox4Menu(message)


@router.message(StatusFilter(3), F.text.contains("Фотофиксация"))
async def ButtonBack(message: Message):
    userID = message.from_user.id
    ID = await SelectValues("request", "users", "userID = (?)", [userID])
    additionally = await SelectValues("status, editable",
                                      "requests",
                                      "ID = (?)",
                                      [int(ID[0][0])])
    if additionally[0][1] == 0:
        await message.answer("Ни-ни... Запрос уже обработан!")
        return

    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 35)
    await OutputBox5Menu(message)


@router.message(StatusFilter(3), F.text.contains("Подробности"))
async def ButtonBack(message: Message):
    userID = message.from_user.id
    ID = await SelectValues("request", "users", "userID = (?)", [userID])
    additionally = await SelectValues("status, editable",
                                      "requests",
                                      "ID = (?)",
                                      [int(ID[0][0])])
    if additionally[0][1] == 0:
        await message.answer("Ни-ни... Запрос уже обработан!")
        return

    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 36)
    await OutputBox6Menu(message)


async def OutputInputFormMenu(message: Message):
    ID = await SelectValues("request", "users", "userID = (?)", [message.from_user.id])
    additionally = await SelectValues("editable, htmlText",
                                      "requests",
                                      "ID = (?)",
                                      [int(ID[0][0])])
    boxs = await SelectValues("box1, box2, box3, box4, box5, box6",
                              "requests",
                              "ID = (?)",
                              [int(ID[0][0])])
    if additionally[0][0] == 1:
        kb = [
            [
                KeyboardButton(text=f"✍️ [Ваш ник]: {"✖" if boxs[0][0] == "-" else "✔"}"),
                KeyboardButton(text=f"👤 [Нарушитель]: {"✖" if boxs[0][1] == "-" else "✔"}")
            ],
            [
                KeyboardButton(text=f"📋 [Тип нарушения]: {"✖" if boxs[0][2] == "-" else "✔"}"),
                KeyboardButton(text=f"🌐 [Координаты]: {"✖" if boxs[0][3] == "-" else "✔"}")
            ],
            [
                KeyboardButton(text=f"📷 [Фотофиксация]: {"✖" if boxs[0][4] == "-" else "✔"}"),
                KeyboardButton(text=f"📚 [Подробности]: {"✖" if boxs[0][5] == "-" else "✔"}")
            ],
            [
                KeyboardButton(text=f"◀ [Назад]"),
                KeyboardButton(text=f"[Сохранить] ▶")
            ]
        ]
        text = await PreviewText(message, ID, boxs)
    else:
        kb = [[KeyboardButton(text=f"◀ [Назад]")]]
        text = additionally[0][1]
    placeholder = "Выберите поле для редактирования:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)

    messageID = await message.answer(text, reply_markup=Keys)

    if boxs[0][4] != "-":
        splitListing = boxs[0][4].split("\n")
        existing_photos = [path for path in splitListing if os.path.exists(path)]
        if existing_photos:
            media = [InputMediaPhoto(media=FSInputFile(path)) for path in existing_photos]
            await message.answer_media_group(
                media=media,
                reply_to_message_id=messageID.message_id
            )


async def PreviewText(message: Message, ID, boxs):

    additionally = await SelectValues("editable, htmlText",
                                      "requests",
                                      "ID = (?)",
                                      [int(ID[0][0])])
    if additionally[0][0] == 1:
        separator = "--------------------------------\n"

        # Составление обязательной структуры жалобы
        text = (f"<b>Запрос №{int(ID[0][0]):03d}:</b> ⚙\n"
                f"{separator}"
                f"  <b>1) Ник игрока:</b> {boxs[0][0]}\n"
                f"  <b>2) Ник нарушителя:</b> {boxs[0][1]}\n"
                f"  <b>3) Тип нарушения:</b> {boxs[0][2]}\n")

        # Добавление необязательной структуры жалобы, где index - номер пункта
        index = 3

        if boxs[0][3] != "-":
            index += 1
            text += f"  <b>{index}) Координаты:</b> {boxs[0][3]}\n"
        if boxs[0][5] != "-":
            index += 1
            text += f"  <b>{index}) Подробности:</b> {boxs[0][5]}\n"
        if boxs[0][4] != "-":
            index += 1
            text += f"  <b>{index}) Фотофиксация:</b> {"-" if boxs[0][4] == "-" else "✅"}\n"

        # Гипперссылка для {✍️ Написано: fullname}
        botLink = "<a href='https://t.me/MineSlopeBot'>✍️</a>"

        fullName = message.from_user.full_name
        user_link = (
            f"<a href='https://t.me/{message.from_user.username}'>{fullName}</a>"
            if message.from_user.username
            else fullName
        )

        text += (f"{separator}"
                 f"{botLink} <b>Написано</b>: {user_link}\n"
                 f"{separator}")
    else:
        text = additionally[0][1]

    return text
