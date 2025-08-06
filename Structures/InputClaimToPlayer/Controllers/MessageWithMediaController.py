import os

from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InputMediaPhoto, FSInputFile, \
    InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from SQLite.DeleteValues import DeleteValues
from SQLite.SelectValues import SelectValues
from SQLite.UpdateValues import UpdateValues
from Structures.InputClaimToPlayer.AutoReplies import RequestBeenProcessed, TextEdited, PhotoEdited, RequestCreating


async def SaveButtonController(message: Message, text: str, ID: int, boxs: list):
    originalID = 0 - ID
    original = await SelectValues("editable, messageID, mediaID, htmlText, box5", "requests", "ID = (?)",
                                  [originalID])

    # Проверка на актуальное редактирование оригинальной жалобы
    if original[0][0] == 0:
        await message.answer(RequestBeenProcessed)
        await DeleteValues("requests", "ID = (?)", [ID])
        return

    # Если оригинальный htmlText отличается от текущего htmlText - изменение!
    if original[0][3] != text:
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(
            text="⚙ Действия",
            callback_data="actions"
        ))

        await message.bot.edit_message_text(chat_id=-1002691896200, message_id=original[0][1], text=text,
                                            reply_markup=keyboard.as_markup())
        await UpdateValues("requests", "box1 = (?), box2 = (?), box3 = (?), box4 = (?), box6 = (?),"
                                       "htmlText = (?)", "ID = (?)",
                           [boxs[0][0], boxs[0][1], boxs[0][2], boxs[0][3], boxs[0][5], text,
                            originalID])
        await message.answer(TextEdited)

    # Если оригинальные фото отличаются от текущего - изменение!
    if boxs[0][4] != original[0][4]:

        mediaID = original[0][2].split("\n")
        box5 = boxs[0][4].split("\n")
        originalBox5 = original[0][4].split("\n")

        # Если изменяется меньшее количество картинок или равное:
        if len(box5) <= len(originalBox5) and originalBox5[0] != "-":
            newMediaID = "-"
            for i in range(len(mediaID)):
                # Удаление лишнего фото (Если текущих фото меньше оригинальных, или если вообще были удалены
                if i >= len(box5) or box5[i] == "-":
                    try:
                        await message.bot.delete_message(
                            chat_id=-1002691896200,
                            message_id=int(mediaID[i]))
                    # Если сообщение уже удалено
                    except:
                        continue
                # Если возможно заменить фотографии
                else:
                    # Если фото отличается и путь до файла существует!
                    if box5[i] != originalBox5[i] and os.path.exists(box5[i]):
                        try:
                            await message.bot.edit_message_media(
                                chat_id=-1002691896200,
                                message_id=int(mediaID[i]),
                                media=InputMediaPhoto(media=FSInputFile(box5[i])))
                        except:
                            continue
                    if newMediaID == "-":
                        newMediaID = f"{mediaID[i]}"
                    else:
                        newMediaID = f"\n{mediaID[i]}"
            await UpdateValues("requests", "mediaID = ?", "ID = ?",
                               [newMediaID, int(originalID)])
        else:

            existing_photos = [path for path in box5 if os.path.exists(path)]
            if existing_photos:
                # Удаляем старые сообщения
                if original[0][4] != "-":
                    for CopyMediaID in mediaID:
                        try:
                            await message.bot.delete_message(
                                chat_id=-1002691896200,
                                message_id=int(CopyMediaID))
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

        await UpdateValues("requests", "box5 = (?)", "ID = (?)",
                           [boxs[0][4], originalID])
        await message.answer(PhotoEdited)
    await DeleteValues("requests", "ID = (?)", [ID])


async def CreatingButtonController(message: Message, text: str, ID: int, box5: str):
    await UpdateValues("requests", "status = 'await', htmlText = (?)", "ID = (?)",
                       [text, ID])
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
    await UpdateValues("requests", "messageID = (?)", "ID = (?)", [messageID.message_id, ID])

    # Список фото (локальные пути)
    if box5 != "-":
        splitListing = box5.split("\n")
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
            await UpdateValues("requests", "mediaID = (?)", "ID = (?)", [mediaID, ID])
    await message.answer(RequestCreating)


async def OutputMessageWithMedia(message: Message, text: str, keys: ReplyKeyboardMarkup, box4):

    messageID = await message.answer(text, reply_markup=keys)

    if box4 != "-":
        splitListing = box4.split("\n")
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
        text = (f"{separator}"
                f"<b>Жалоба №{abs(int(ID[0][0])):03d}:</b> ⚙\n"
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
