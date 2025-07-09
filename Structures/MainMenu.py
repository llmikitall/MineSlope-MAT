from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

from aiogram import Router

from Middlewares.PrivateChatMiddleware import PrivateChatMiddleware

router = Router()
router.message.middleware(PrivateChatMiddleware())


@router.message(F.text.contains("Отправить жалобу")) #, StatusFilter("1"))
async def SendMessageClaim(message: Message):

    from Structures.SendMessageMenu import OutputSendMessageMenu
    await OutputSendMessageMenu(message)


async def OutputMainMenu(message: Message):

    sep = "-------------------------------------------------------\n"
    text = ("   [<b>Добро пожаловать в главное меню!</b>]\n   Здесь <i>Вы</i> можете отправить жалобу на игрока "
            "и-и-и... <b>пока</b> на этом всё. Но это тестовая секретная разработка!!\n"
            "   Примечание: Данное приветствующее сообщение будет показываться лишь 1-н раз для "
            "новых пользователей бота, при повторном нажатии на /start не будет показываться. (Не реализовано ещё)\n")
    await message.answer(sep + text + sep)

    kb = [
        [KeyboardButton(text="Отправить жалобу")]
        # [KeyboardButton(text=f"{emojiList[3]}Факультатив"), KeyboardButton(text=f"{emojiList[3]}Поиск")],
        # [KeyboardButton(text=f"{emojiList[2]}Настройки")],
        # [KeyboardButton(text=f"{emojiList[4]}Поменять группу: {userGroup}")]
    ]
    placeholder = "Выберите желаемое действие:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("[Главное меню]", reply_markup=Keys)

