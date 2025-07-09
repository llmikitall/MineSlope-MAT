from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

from aiogram import Router

from Middlewares.PrivateChatMiddleware import PrivateChatMiddleware

router = Router()
router.message.middleware(PrivateChatMiddleware())


STATUS = 0
VALUES = list()
VALUES.append("6609070015")
VALUES.append("4")


@router.message(F.text.contains("Назад")) #, StatusFilter("1"))
async def SendMessageClaim(message: Message):
    # global STATUS
    # STATUS = 0
    # from SQLite.InsertValues import InsertValues
    # await InsertValues("requests", values=VALUES)
    from Structures.MainMenu import OutputMainMenu
    await OutputMainMenu(message)


'''
@router.message(F.text.contains("Ваш ник")) #, StatusFilter("1"))
async def SmallStatus1(message: Message):
    global STATUS
    STATUS = 1


@router.message()
async def statusMessage(message: Message):
    if STATUS == 0:
        await message.answer("Выберите пункт!")
    elif STATUS != 0:
        VALUES.append(message.text)

'''


async def OutputSendMessageMenu(message: Message):

    sep = "-------------------------------------------------------\n"
    text = ("   Вы открыли секретную функцию секретного бота! Но она пока не работает... смиритесь."
            "\n   Зато здесь будет выскакивать сообщение: \"Введите одно, введите другое!\", и если игрок"
            " передумает писать отчёт, то он может просто спокойно нажать на кнопку \"Отмена\" и вернуться "
            "обратно в меню. Кнопка сейчас уже есть.\n")
    await message.answer(sep + text + sep)

    kb = [
        [KeyboardButton(text="Ваш ник")],
        [KeyboardButton(text="Ник нарушителя")],
        [KeyboardButton(text="Тип нарушения")],
        [KeyboardButton(text="Координаты нарушения")],
        [KeyboardButton(text="Доказательства")],
        [KeyboardButton(text="Назад")]
        # [KeyboardButton(text=f"{emojiList[3]}Факультатив"), KeyboardButton(text=f"{emojiList[3]}Поиск")],
        # [KeyboardButton(text=f"{emojiList[2]}Настройки")],
        # [KeyboardButton(text=f"{emojiList[4]}Поменять группу: {userGroup}")]
    ]
    placeholder = "Выберите желаемое действие:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("[Отправка жалобы...]", reply_markup=Keys)