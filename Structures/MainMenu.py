from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

from aiogram import Router

from Middlewares.PrivateChatMiddleware import PrivateChatMiddleware
from StatusFilter import StatusFilter

router = Router()
router.message.middleware(PrivateChatMiddleware())


@router.message(F.text.contains("Отправить жалобу"), StatusFilter(1))
async def SendMessageClaim(message: Message):
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 2)
    from Structures.ClaimToPlayerMenu import OutputClaimToPlayer
    await OutputClaimToPlayer(message)


async def OutputMainMenu(message: Message):

    from SQLite.SelectValues import FindAnyRowUsers
    if FindAnyRowUsers(message.from_user.id, "oMainMenu") == 0:
        sep = "-------------------------------------------------------\n"
        text = ("   [<b>fraysad!</b>]\n   Новое обновление бота. Считай, что v0.2. Что изменилось? Можешь посмотреть "
                "сам увидеть и потрогать!\n   Во-первых, это сообщение ты увидишь единожды, если опять нажмёшь "
                "/start, или вернёшься в меню, то его больше не увидишь. Тут можно написать приветствие или "
                "кратко объяснить суть бота. \n   Во-вторых, я таки сделал первый образец составления жалобы. "
                "Как только нажмёшь 'Создать запрос', то ты увидишь 6 кнопок (пока что), после каждой из них "
                "будет написано '-'. Нажимай на каждую кнопку, и вводи интересующуюся информацию. В результате "
                "увидишь что изменится. Созданный запрос ты не увидишь, зато увижу я. Он создаётся в базу данных и "
                "там лежит. Опять же, это ещё сырая версия, считай, что это лишь скелет того, как будет"
                " работать.\n")
        await message.answer(sep + text + sep)
        from SQLite.UpdateValues import UpdateValue
        UpdateValue(message.from_user.id, "users", "oMainMenu", 1)

    kb = [
        [KeyboardButton(text="Отправить жалобу")]
    ]
    placeholder = "Выберите желаемое действие:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("[Главное меню]", reply_markup=Keys)

