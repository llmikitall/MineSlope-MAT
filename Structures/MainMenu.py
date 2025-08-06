from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

from aiogram import Router

from Filters.PrivateChatFilter import PrivateChatFilter
from Structures.MenuNavigator import OutputClaimToPlayerMenu
from Filters.StatusFilter import StatusFilter
from Structures.ClaimToPlayerMenu import router as claim_to_player_router

router = Router()
router.include_routers(claim_to_player_router)


@router.message(StatusFilter(1), F.text.contains("Отправить жалобу"))
async def SendMessageClaim(message: Message):
    from SQLite.UpdateValues import UpdateValue
    UpdateValue(message.from_user.id, "users", "status", 2)
    await OutputClaimToPlayerMenu(message)


async def OutputMainMenu(message: Message):

    from SQLite.SelectValues import FindAnyRowUsers
    if FindAnyRowUsers(message.from_user.id, "oMainMenu") == 0:
        sep = "-------------------------------------------------------\n"
        text = ("<b>[Добро пожаловать!]</b>\n"
        "   Я - Минеслопик. Помогаю игрокам, упрощая работу нашей администрации"
        " и игрокам! Умею на данный момент только составлять жалобы...\n"
        "   <i>Прошу, не будьте ко мне строги!</i>\n")
        await message.answer(sep + text + sep)
        from SQLite.UpdateValues import UpdateValue
        UpdateValue(message.from_user.id, "users", "oMainMenu", 1)

    kb = [
        [KeyboardButton(text="🚨 [Отправить жалобу]")]
    ]
    placeholder = "Выберите желаемое:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("<b>[Главное меню]</b>", reply_markup=Keys)

