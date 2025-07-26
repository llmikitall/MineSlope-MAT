from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

from aiogram import Router

from Filters.StatusFilter import StatusFilter
from SQLite.UpdateValues import UpdateValue
from SQLite.InsertValues import InsertValues
from SQLite.SelectValues import FindMaxRequest, SelectValues
from Structures.MenuNavigator import OutputInputFormMenu, OutputMainMenu
from Structures.InputClaimToPlayer.InputFormMenu import router as input_form_router
from SQLite.SelectValues import FindExitsRow


router = Router()
router.include_router(input_form_router)


@router.message(StatusFilter(2), F.text.contains("Назад"))
async def ButtonBack(message: Message):
    # Кнопка делает status пользователя = 1 и возвращает в главное меню
    UpdateValue(message.from_user.id, "users", "status", 1)
    await OutputMainMenu(message)


@router.message(StatusFilter(2), F.text.contains("Создать"))
async def ButtonCreate(message: Message):
    # Кнопка создать создаёт новую строчку в requests, меняет status и указывает в request номер созданного запроса
    userID = message.from_user.id

    await InsertValues("requests",
                       "(userID, topicID)",
                       "(?, ?)",
                       (userID, "4"))

    UpdateValue(userID, "users", "request", str(FindMaxRequest(userID)))

    UpdateValue(userID, "users", "status", 3)
    await OutputInputFormMenu(message)


@router.message(StatusFilter(2), F.text.contains("Запрос №"))
async def ButtonRequest(message: Message):
    # Получаем номер запроса, который ввёл пользователь
    userID = message.from_user.id

    # Проверка от букв и SQL-инъекции
    try:
        ID = int(message.text.split("№")[1])
    except (IndexError, ValueError):
        await message.answer(f"<b>[Некорректный номер запроса]</b>:")
        return

    # Проверяем наличие такого запроса. (Тут нужно переделать...
    #   ...надо SELECT ID FROM requests WHERE userID = ?; и код сократится)
    if await FindExitsRow("requests", "ID", int(ID)) == 0:
        await message.answer("<b>[Запрос не найден или не принадлежит Вам]</b>:")
        return

    # Изменяем request и status пользователя
    UpdateValue(userID, "users", "request", int(ID))

    UpdateValue(userID, "users", "status", 3)
    await OutputInputFormMenu(message)


async def OutputClaimToPlayer(message: Message):
    userID = message.from_user.id

    # Создаём кнопку "Создать..." в самый верх
    kb = [[KeyboardButton(text="Создать новую жалобу")]]

    # Получаем все запросы пользователя и сортируем (чтобы более новые запросы были сверху)
    listing = await SelectValues("ID, status", "requests", "userID = (?)", [str(userID)])
    listing.sort(reverse=True)

    for i in range(len(listing)):
        emoji = "⚙"
        if listing[i][1] == "accept":
            emoji = "✅"
        elif listing[i][1] == "deny":
            emoji = "❌"
        elif listing[i][1] == "viewing":
            emoji = "🔍"

        kb.append([KeyboardButton(text=f"{emoji} Запрос №{listing[i][0]:03d}")])

    kb.append([KeyboardButton(text="Назад")])

    # Оформляем вывод
    placeholder = "Выберите жалобу:"
    Keys = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder=placeholder)
    await message.answer("<b>[Текущие Ваши запросы]</b>:", reply_markup=Keys)
