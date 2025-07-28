import os

from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, \
    FSInputFile
from aiogram import F

from aiogram import Router
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Filters.StatusFilter import StatusFilter
from SQLite.DeleteValues import DeleteValues
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
from Structures.InputClaimToPlayer.AutoReplies import RequestBeenProcessed

router = Router()
router.include_routers(box1_router, box2_router, box3_router, box4_router, box5_router, box6_router)


# Удаление при creating и editing!
@router.message(StatusFilter(3), F.text.contains("Назад"))
async def ButtonBack(message: Message):
    userID = message.from_user.id
    request = await SelectValues("request", "users", "userID = (?);", [userID])
    status = await SelectValues("status", "requests", "ID = (?) AND userID = (?);", [int(request[0][0]), str(userID)])
    if status[0][0] == "creating" or int(request[0][0]) < 0:
        await DeleteValues("requests", "ID = (?)", [int(request[0][0])])
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
        await message.answer(RequestBeenProcessed)
        return

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

    if int(ID[0][0]) < 0:
        originalID = 0 - int(ID[0][0])
        original = await SelectValues("editable, messageID, mediaID, htmlText, box5", "requests", "ID = (?)",
                                      [originalID])
        if original[0][0] == 0:
            await message.answer(RequestBeenProcessed)

        else:
            if original[0][3] != text:
                await UpdateValues("requests", "box1 = (?), box2 = (?), box3 = (?), box4 = (?), box6 = (?),"
                                               "htmlText = (?)", "ID = (?)",
                                   [boxs[0][0], boxs[0][1], boxs[0][2], boxs[0][3], boxs[0][5], text,
                                    originalID])
                keyboard = InlineKeyboardBuilder()
                keyboard.add(InlineKeyboardButton(
                    text="⚙ Действия",
                    callback_data="actions"
                ))

                await message.bot.edit_message_text(chat_id=-1002691896200, message_id=original[0][1], text=text,
                                                    reply_markup=keyboard.as_markup())
                await message.answer("<b>[Текст запроса был успешно отредактирован]</b>")
            if boxs[0][4] != original[0][4]:
                await UpdateValues("requests", "box5 = (?)", "ID = (?)",
                                   [boxs[0][4], originalID])
                mediaID = original[0][2].split("\n")
                box5 = boxs[0][4].split("\n")
                originalBox5 = original[0][4].split("\n")
                if len(box5) <= len(originalBox5):
                    for i in range(len(mediaID)):
                        if i >= len(box5) or box5[i] == "-":
                            # Удаляем лишние фото
                            try:
                                await message.bot.delete_message(
                                    chat_id=-1002691896200,
                                    message_id=int(mediaID[i]))
                            except:
                                continue  # Если сообщение уже удалено
                        else:
                            if originalBox5[i] == "-":
                                new_messages = await message.bot.send_media_group(
                                    chat_id=-1002691896200,
                                    message_thread_id=4,
                                    media=[InputMediaPhoto(media=FSInputFile(path)) for path in box5],
                                    reply_to_message_id=int(original[0][1]))
                                new_ids = "\n".join(str(msg.message_id) for msg in new_messages)
                                await UpdateValues("requests", "mediaID = ?", "ID = ?",
                                                   [new_ids, int(originalID)])
                            # Редактируем только если фото ИЗМЕНИЛОСЬ
                            elif box5[i] != originalBox5[i] and os.path.exists(box5[i]):
                                try:
                                    await message.bot.edit_message_media(
                                        chat_id=-1002691896200,
                                        message_id=int(mediaID[i]),
                                        media=InputMediaPhoto(media=FSInputFile(box5[i])))
                                except Exception as e:
                                    print(f"Ошибка редактирования: {e}")
                    if len(box5) < len(originalBox5):
                        if box5[0] == "-":
                            new_ids = "-"
                        else:
                            new_ids = f"{mediaID[0]}"
                            for i in range(1, len(box5)):
                                new_ids = f"\n{mediaID[i]}"
                        await UpdateValues("requests", "mediaID = ?", "ID = ?",
                                           [new_ids, int(originalID)])
                else:
                    existing_photos = [path for path in box5 if os.path.exists(path)]
                    if existing_photos:
                        # Удаляем старые сообщения
                        for msg_id in mediaID:
                            try:
                                await message.bot.delete_message(
                                    chat_id=-1002691896200,
                                    message_id=int(msg_id))
                            except:
                                continue

                        # Отправляем новый альбом
                        media = [InputMediaPhoto(media=FSInputFile(path)) for path in existing_photos]
                        new_messages = await message.bot.send_media_group(
                            chat_id=-1002691896200,
                            message_thread_id=4,
                            media=media,
                            reply_to_message_id=int(original[0][1]))

                        # Обновляем ID в базе
                        new_ids = "\n".join(str(msg.message_id) for msg in new_messages)
                        await UpdateValues("requests", "mediaID = ?", "ID = ?",
                                           [new_ids, int(originalID)])
                await message.answer("<b>[Фото запроса было успешно отредактировано]</b>")
        await DeleteValues("requests", "ID = (?)", [int(ID[0][0])])
    elif additionally[0][0] == "creating":
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
                mediaIDMessage = await message.bot.send_media_group(
                    chat_id=-1002691896200,
                    message_thread_id=4,
                    media=media,
                    reply_to_message_id=messageID.message_id  # Привязка к тексту
                )
                mediaIDList = [msg.message_id for msg in mediaIDMessage]
                mediaID = f"{mediaIDList[0]}"
                for i in range(1, len(mediaIDList)):
                    mediaID += f"\n{mediaIDList[i]}"
                await UpdateValues("requests", "mediaID = (?)", "ID = (?)", [mediaID, int(ID[0][0])])
        await message.answer("<b>[Ваш запрос был успешно составлен]</b>\nПожалуйста, ожидайте обратной связи.")

    UpdateValue(message.from_user.id, "users", "request", "-")
    UpdateValue(message.from_user.id, "users", "status", 1)
    await OutputMainMenu(message)


@router.message(StatusFilter(3), F.text.contains("Мой ник"))
async def ButtonBack(message: Message):
    userID = message.from_user.id
    ID = await SelectValues("request", "users", "userID = (?)", [userID])
    additionally = await SelectValues("status, editable",
                                      "requests",
                                      "ID = (?)",
                                      [int(ID[0][0])])
    if additionally[0][1] == 0:
        await message.answer(RequestBeenProcessed)
        return

    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 31)
    await OutputBox1Menu(message)


@router.message(StatusFilter(3), F.text.contains("Его ник"))
async def ButtonBack(message: Message):
    userID = message.from_user.id
    ID = await SelectValues("request", "users", "userID = (?)", [userID])
    additionally = await SelectValues("status, editable",
                                      "requests",
                                      "ID = (?)",
                                      [int(ID[0][0])])
    if additionally[0][1] == 0:
        await message.answer(RequestBeenProcessed)
        return
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 32)
    await OutputBox2Menu(message)


@router.message(StatusFilter(3), F.text.contains("Тип"))
async def ButtonBack(message: Message):
    userID = message.from_user.id
    ID = await SelectValues("request", "users", "userID = (?)", [userID])
    additionally = await SelectValues("status, editable",
                                      "requests",
                                      "ID = (?)",
                                      [int(ID[0][0])])
    if additionally[0][1] == 0:
        await message.answer(RequestBeenProcessed)
        return

    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 33)
    await OutputBox3Menu(message)


@router.message(StatusFilter(3), F.text.contains("Коорд."))
async def ButtonBack(message: Message):
    userID = message.from_user.id
    ID = await SelectValues("request", "users", "userID = (?)", [userID])
    additionally = await SelectValues("status, editable",
                                      "requests",
                                      "ID = (?)",
                                      [int(ID[0][0])])
    if additionally[0][1] == 0:
        await message.answer(RequestBeenProcessed)
        return

    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 34)
    await OutputBox4Menu(message)


@router.message(StatusFilter(3), F.text.contains("Фото"))
async def ButtonBack(message: Message):
    userID = message.from_user.id
    ID = await SelectValues("request", "users", "userID = (?)", [userID])
    additionally = await SelectValues("status, editable",
                                      "requests",
                                      "ID = (?)",
                                      [int(ID[0][0])])
    if additionally[0][1] == 0:
        await message.answer(RequestBeenProcessed)
        return

    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 35)
    await OutputBox5Menu(message)


@router.message(StatusFilter(3), F.text.contains("Детали"))
async def ButtonBack(message: Message):
    userID = message.from_user.id
    ID = await SelectValues("request", "users", "userID = (?)", [userID])
    additionally = await SelectValues("status, editable",
                                      "requests",
                                      "ID = (?)",
                                      [int(ID[0][0])])
    if additionally[0][1] == 0:
        await message.answer(RequestBeenProcessed)
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
                KeyboardButton(text=f"👤 [Мой ник]: {'✖' if boxs[0][0] == '-' else '✔'}"),
                KeyboardButton(text=f"💢 [Его ник]: {'✖' if boxs[0][1] == '-' else '✔'}")
            ],
            [
                KeyboardButton(text=f"📌 [Тип]: {'✖' if boxs[0][2] == '-' else '✔'}"),
                KeyboardButton(text=f"🌐 [Коорд.]: {'✖' if boxs[0][3] == '-' else '✔'}")
            ],
            [
                KeyboardButton(text=f"📷 [Фото]: {'✖' if boxs[0][4] == '-' else '✔'}"),
                KeyboardButton(text=f"📋 [Детали]: {'✖' if boxs[0][5] == '-' else '✔'}")
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
    placeholder = "Выберите поле:"
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
        text = (f"<b>Запрос №{abs(int(ID[0][0])):03d}:</b> ⚙\n"
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
            text += f"  <b>{index}) Фотофиксация:</b> {'-' if boxs[0][4] == '-' else '✅'}\n"

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
