import os

import aiogram.exceptions
from aiogram.types import Message, ReplyKeyboardMarkup, InputMediaPhoto, FSInputFile, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from SQLite.DeleteValues import DeleteValues
from SQLite.SelectValues import SelectValues
from SQLite.UpdateValues import UpdateValues
from Structures.InputClaimToPlayer.AutoReplies import RequestCreating, RequestBeenProcessed, TextEdited, PhotoEdited

from Callbacks.ClaimToPlayer.MediaWithMessage import router


async def SaveButtonController(message: Message, text: str, ID: int, boxs: list):
    originalID = abs(ID)
    original = await SelectValues("editable, messageID, mediaID, htmlText, box5", "requests", "ID = (?)",
                                  [originalID])
    originalText = original[0][3].split("[statusText]\n")
    # Проверка на актуальное редактирование оригинальной жалобы
    if original[0][0] == 0:
        await message.answer(RequestBeenProcessed)
        return
    edit = "<i>Жалоба была отредактирована</i>\n"
    statusText = await PreviewStatusText(message)
    if edit not in statusText:
        statusText = statusText + edit
    # Если оригинальный htmlText отличается от текущего htmlText - изменение!
    if originalText[0] != text or boxs[0][4] != original[0][4]:
        await UpdateValues("requests", "box1 = (?), box2 = (?), box3 = (?), box4 = (?), box5 = (?), box6 = (?)",
                           "ID = (?)",
                           [boxs[0][0], boxs[0][1], boxs[0][2], boxs[0][3], boxs[0][4], boxs[0][5], originalID])

        try:
            await message.bot.delete_message(chat_id=-1002691896200, message_id=original[0][1])
        except aiogram.exceptions.TelegramBadRequest:
            print("[<] Сообщение уже было удалено")

        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(
            text="⚙ Действия",
            callback_data="actions"
        ))

        if boxs[0][4] == "-":
            mediaID = original[0][2].split("\n")
            for msg in mediaID:
                try:
                    await message.bot.delete_message(chat_id=-1002691896200, message_id=int(msg))
                except aiogram.exceptions.TelegramBadRequest:
                    print("[<] Сообщение уже было удалено")
                    continue

            mediaID = await message.bot.send_message(text=text,
                                                     chat_id=-1002691896200,
                                                     message_thread_id=4)
            mediaID = mediaID.message_id
            messageID = await message.bot.send_message(text=statusText,
                                                       chat_id=-1002691896200,
                                                       message_thread_id=4,
                                                       reply_markup=keyboard.as_markup())
            messageID = messageID.message_id

        else:
            box5 = boxs[0][4].split("\n")
            mediaID = original[0][2].split("\n")
            for msg in mediaID:
                await message.bot.delete_message(
                    chat_id=-1002691896200,
                    message_id=int(msg))

            existing_photos = [path for path in box5 if os.path.exists(path)]

            media = [InputMediaPhoto(
                media=FSInputFile(existing_photos[0]),
                caption=text,
            )]

            existing_photos.remove(existing_photos[0])

            if len(box5) >= 1:
                media += [InputMediaPhoto(media=FSInputFile(path)) for path in existing_photos]

            mediaIDList = await message.bot.send_media_group(
                chat_id=-1002691896200,
                message_thread_id=4,
                media=media
            )
            mediaIDList = [msg.message_id for msg in mediaIDList]
            mediaID = ""
            for i in mediaIDList:
                if mediaIDList[0] == i:
                    mediaID = f"{i}"
                    continue
                mediaID += f"\n{i}"

            messageID = await message.bot.send_message(text=statusText,
                                                       chat_id=-1002691896200,
                                                       message_thread_id=4,
                                                       reply_markup=keyboard.as_markup())
            messageID = messageID.message_id

        await UpdateValues("requests", "messageID = (?), mediaID = (?), htmlText = (?)", "ID = (?)",
                           [messageID, mediaID, f"{text}[statusText]\n{statusText}", int(originalID)])
        await message.answer(TextEdited)

    await DeleteValues("requests", "ID = (?)", [ID])


async def CreatingButtonController(message: Message, ID: int, boxs):
    text = await PreviewText(ID, boxs)
    await UpdateValues("requests", "status = 'await'", "ID = (?)", [ID])

    if boxs[0][4] == "-":
        mediaID = await message.bot.send_message(text=text,
                                                 chat_id=-1002691896200,
                                                 message_thread_id=4
                                                 )
        mediaID = mediaID.message_id
        await UpdateValues("requests", "mediaID = (?)", "ID = (?)", [mediaID, ID])
    else:
        splitBox5 = boxs[0][4].split("\n")
        existing_photos = [path for path in splitBox5 if os.path.exists(path)]

        media = [InputMediaPhoto(
            media=FSInputFile(existing_photos[0]),
            caption=text,
        )]
        existing_photos.remove(existing_photos[0])

        if len(splitBox5) >= 1:
            media += [InputMediaPhoto(media=FSInputFile(path)) for path in existing_photos]

        mediaIDList = await message.bot.send_media_group(
            chat_id=-1002691896200,
            message_thread_id=4,
            media=media
        )
        mediaID = [msg.message_id for msg in mediaIDList]
        mediaIDstr = ""
        for i in mediaID:
            if mediaID[0] == i:
                mediaIDstr = f"{i}"
                continue
            mediaIDstr += f"\n{i}"
        await UpdateValues("requests", "mediaID = (?)", "ID = (?)", [mediaIDstr, ID])
    statusText = await PreviewStatusText(message)

    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
        text="⚙ Действия",
        callback_data="actions"
    ))

    messageID = await message.bot.send_message(
        chat_id=-1002691896200,
        message_thread_id=4,
        text=statusText,
        reply_markup=keyboard.as_markup()
    )
    htmlText = f"{text}[statusText]\n{statusText}"
    await UpdateValues("requests", "messageID = (?)", "ID = (?)", [messageID.message_id, ID])
    await UpdateValues("requests", "htmlText = (?)", "ID = (?)", [htmlText, ID])
    await message.answer(RequestCreating)

    return


async def OutputMediaWithMessage(message: Message, text: str, keys: ReplyKeyboardMarkup, box5):
    if box5 == "-":
        mediaID = await message.answer(text, reply_markup=keys)
        mediaID = mediaID.message_id
    else:
        splitBox5 = box5.split("\n")
        existing_photos = [path for path in splitBox5 if os.path.exists(path)]

        media = [InputMediaPhoto(
            media=FSInputFile(existing_photos[0]),
            caption=text,
        )]
        existing_photos.remove(existing_photos[0])

        if len(splitBox5) >= 1:
            media += [InputMediaPhoto(media=FSInputFile(path)) for path in existing_photos]
        mediaIDList = await message.answer_media_group(
            media=media,
        )
        mediaID = [msg.message_id for msg in mediaIDList][0]

    statusText = await PreviewStatusText(message)

    messageID = await message.answer(statusText, reply_markup=keys)
    return


async def PreviewText(ID, boxs):
    additionally = await SelectValues("editable, htmlText",
                                      "requests",
                                      "ID = (?)",
                                      [ID])
    if additionally[0][0] == 1:
        separator = "--------------------------------\n"

        # Составление обязательной структуры жалобы
        text = (f"<b>Жалоба №{abs(ID):03d}:</b>\n"
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
            text += f"  <b>{index}) Детали:</b> {boxs[0][5]}\n"
        if boxs[0][4] != "-":
            index += 1
            text += f"  <b>{index}) Фотофиксация:</b> {'-' if boxs[0][4] == '-' else '✅'}\n"
    else:
        text = additionally[0][1]

    return text


async def PreviewStatusText(message: Message):
    ID = await SelectValues("request", "users", "userID = (?)", [message.from_user.id])
    additionally = await SelectValues("status",
                                      "requests",
                                      "ID = (?)",
                                      [int(ID[0][0])])
    separator = "--------------------------------\n"
    if additionally[0][0] == "creating":
        status = "📋 Создание жалобы"
    elif additionally[0][0] == "await":
        status = "⚙ Ожидание действий"
    elif additionally[0][0] == "accept":
        status = "✅ Успешно обработана"
    elif additionally[0][0] == "deny":
        status = "❌ Отклонена"
    else:
        status = "🔍 На рассмотрении"
    # Составление обязательной структуры жалобы
    text = f"<b>Статус жалобы №{abs(int(ID[0][0])):03d}</b>: {status}\n"

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

    return text
