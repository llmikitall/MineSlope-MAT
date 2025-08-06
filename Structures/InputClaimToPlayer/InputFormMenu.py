import os
import re

from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

from aiogram import Router

from Filters.StatusFilter import StatusFilter
from SQLite.DeleteValues import DeleteValues
from Structures.InputClaimToPlayer.Controllers.MediaWithMessageController import (OutputMediaWithMessage, PreviewText,
                                                                                  CreatingButtonController,
                                                                                  SaveButtonController)


from Structures.MenuNavigator import (OutputClaimToPlayerMenu, OutputBox1Menu, OutputBox2Menu, OutputBox3Menu,
                                      OutputBox4Menu, OutputBox5Menu, OutputBox6Menu, OutputMainMenu)
from SQLite.UpdateValues import UpdateValues
from SQLite.SelectValues import SelectValues
from Structures.InputClaimToPlayer.Box1Menu import router as box1_router
from Structures.InputClaimToPlayer.Box2Menu import router as box2_router
from Structures.InputClaimToPlayer.Box3Menu import router as box3_router
from Structures.InputClaimToPlayer.Box4Menu import router as box4_router
from Structures.InputClaimToPlayer.Box5Menu import router as box5_router
from Structures.InputClaimToPlayer.Box6Menu import router as box6_router
from Structures.InputClaimToPlayer.Controllers.MediaWithMessageController import router as callback_router
from Structures.InputClaimToPlayer.AutoReplies import RequestBeenProcessed, EnterFollowingBoxs


router = Router()
router.include_routers(box1_router, box2_router, box3_router, box4_router, box5_router, box6_router, callback_router)


# Удаление при creating и editing!
@router.message(StatusFilter(3), F.text.contains("Назад"))
async def ButtonBack(message: Message):
    userID = message.from_user.id
    ID = await SelectValues("request", "users", "userID = (?);", [userID])
    status = await SelectValues("status", "requests", "ID = (?) AND userID = (?);", [int(ID[0][0]), str(userID)])
    if status[0][0] == "creating" or int(ID[0][0]) < 0:
        await DeleteValues("requests", "ID = (?)", [int(ID[0][0])])

    await UpdateValues("users", "request = '-', status = 2", "userID = (?)", [str(userID)])
    await OutputClaimToPlayerMenu(message)


@router.message(StatusFilter(3), F.text.contains("Отозвать"))
async def ButtonBack(message: Message):
    # Получение необходимых параметров: userID, ID (requests), boxs, status
    userID = message.from_user.id
    ID = await SelectValues("request", "users", "userID = (?)", [userID])

    additionally = await SelectValues("status,  messageID, htmlText",
                                      "requests",
                                      "ID = (?)",
                                      [int(ID[0][0])])
    if not additionally[0][0] in ("await", "viewing"):
        return await message.answer("<b>На данный момент жалобу нельзя отозвать...</b>")

    emoji = "🚫 Жалоба была отозвана"

    currentText = additionally[0][2].split("[statusText]\n")
    currentText[1] = re.sub(
        r'</b>: .*',
        f'</b>: {emoji}',
        currentText[1],
        count=1
    )
    htmlText = f"{currentText[0]}[statusText]\n{currentText[1]}"
    await UpdateValues("requests", "htmlText = (?)", "ID = (?)", [htmlText, abs(int(ID[0][0]))])

    await message.bot.edit_message_text(text=currentText[1], chat_id=-1002691896200, message_id=additionally[0][1])

    if int(ID[0][0]) < 0:
        await DeleteValues("requests", "ID = (?)", [int(ID[0][0])])
    await message.answer("<b>[Жалоба была успешно отозвана!]</b>")
    await UpdateValues("users", "request = '-', status = 2", "userID = (?)", [str(userID)])
    await OutputClaimToPlayerMenu(message)


@router.message(StatusFilter(3), F.text.contains("Сохранить"))
async def ButtonBack(message: Message):

    # Получение необходимых параметров: userID, ID (requests), boxs, status
    userID = message.from_user.id
    ID = await SelectValues("request", "users", "userID = (?)", [userID])

    boxs = await SelectValues("box1, box2, box3, box4, box5, box6",
                              "requests",
                              "ID = (?)",
                              [int(ID[0][0])])

    additionally = await SelectValues("status",
                                      "requests",
                                      "ID = (?)",
                                      [int(ID[0][0])])

    # Проверки на редактируемость + на не пустые поля
    if await CheckEditable(message):
        return

    check = EnterFollowingBoxs(boxs)
    if check != "":
        await message.answer(check)
        return

    text = await PreviewText(int(ID[0][0]), boxs)

    if int(ID[0][0]) < 0:
        await SaveButtonController(message, text, int(ID[0][0]), boxs)
    elif additionally[0][0] == "creating":
        await CreatingButtonController(message, int(ID[0][0]), boxs)

    await UpdateValues("users", "request = '-', status = 1", "userID = (?)", [str(userID)])
    await OutputMainMenu(message)


@router.message(StatusFilter(3), F.text.contains("Мой ник"))
async def ButtonNick(message: Message):
    if await CheckEditable(message):
        return

    await UpdateValues("users", "status = (?)", "userID = (?)", [31, str(message.from_user.id)])
    await OutputBox1Menu(message)


@router.message(StatusFilter(3), F.text.contains("Его ник"))
async def ButtonIntruder(message: Message):
    if await CheckEditable(message):
        return

    await UpdateValues("users", "status = (?)", "userID = (?)", [32, str(message.from_user.id)])
    await OutputBox2Menu(message)


@router.message(StatusFilter(3), F.text.contains("Тип"))
async def ButtonType(message: Message):
    if await CheckEditable(message):
        return

    await UpdateValues("users", "status = (?)", "userID = (?)", [33, str(message.from_user.id)])
    await OutputBox3Menu(message)


@router.message(StatusFilter(3), F.text.contains("Коорд."))
async def ButtonCoordinate(message: Message):
    if await CheckEditable(message):
        return

    await UpdateValues("users", "status = (?)", "userID = (?)", [34, str(message.from_user.id)])
    await OutputBox4Menu(message)


@router.message(StatusFilter(3), F.text.contains("Фото"))
async def ButtonPhotos(message: Message):
    if await CheckEditable(message):
        return

    await UpdateValues("users", "status = (?)", "userID = (?)", [35, str(message.from_user.id)])
    await OutputBox5Menu(message)


@router.message(StatusFilter(3), F.text.contains("Детали"))
async def ButtonDetails(message: Message):
    if await CheckEditable(message):
        return

    await UpdateValues("users", "status = (?)", "userID = (?)", [36, str(message.from_user.id)])
    await OutputBox6Menu(message)


async def OutputInputFormMenu(message: Message):
    ID = await SelectValues("request", "users", "userID = (?)", [message.from_user.id])
    additionally = await SelectValues("editable, htmlText, status",
                                      "requests",
                                      "ID = (?)",
                                      [int(ID[0][0])])
    boxs = await SelectValues("box1, box2, box3, box4, box5, box6",
                              "requests",
                              "ID = (?)",
                              [int(ID[0][0])])
    kb = []

    if additionally[0][2] in ("await", "viewing"):
        kb.append([KeyboardButton(text="🚫 [Отозвать жалобу]")])

    if additionally[0][0] == 1:
        kb.append([
            KeyboardButton(text=f"👤 [Мой ник]: {'✖' if boxs[0][0] == '-' else '✔'}"),
            KeyboardButton(text=f"💢 [Его ник]: {'✖' if boxs[0][1] == '-' else '✔'}")
        ])
        kb.append([
            KeyboardButton(text=f"📌 [Тип]: {'✖' if boxs[0][2] == '-' else '✔'}"),
            KeyboardButton(text=f"🌐 [Коорд.]: {'✖' if boxs[0][3] == '-' else '✔'}")
        ])
        kb.append([
            KeyboardButton(text=f"📷 [Фото]: {'✖' if boxs[0][4] == '-' else '✔'}"),
            KeyboardButton(text=f"📋 [Детали]: {'✖' if boxs[0][5] == '-' else '✔'}")
        ])
        kb.append([
            KeyboardButton(text="◀ [Назад]"),
            KeyboardButton(text="[Сохранить] ▶")
        ])

        text = await PreviewText(int(ID[0][0]), boxs)
    else:
        kb.append([KeyboardButton(text=f"◀ [Назад]")])
        text = additionally[0][1].split("[statusText]\n")[0]
    placeholder = "Выберите поле:"
    keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)

    await OutputMediaWithMessage(message, text, keys, boxs[0][4])


async def CheckEditable(message: Message):
    ID = await SelectValues("request", "users", "userID = (?)", [message.from_user.id])
    editable = await SelectValues("editable", "requests", "ID = (?)", [int(ID[0][0])])

    if editable == 0:
        await message.answer(RequestBeenProcessed)
        return True
    return False
