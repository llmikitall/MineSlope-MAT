from datetime import datetime
import re

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Callbacks.ClaimToPlayer.AutoReplies import OnlyAdmin
from SQLite.SelectValues import SelectValues
from SQLite.UpdateValues import UpdateValues

router = Router()


@router.callback_query(F.data == "actions_claim")
async def InlineAccept(callback: CallbackQuery):
    if not await is_admin(callback):
        await callback.answer(OnlyAdmin, show_alert=True)
        return

    # Кнопка действия: открывает Принять/Отмена/"На рассмотрении"
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="✅ Принять", callback_data="accept_claim"))
    builder.add(InlineKeyboardButton(text="❌ Отказ", callback_data="denial_claim"))
    builder.add(InlineKeyboardButton(text="🔍 На рассмотрении", callback_data="viewing_claim"))

    builder.adjust(2)

    await callback.message.edit_reply_markup(reply_markup=builder.as_markup())


@router.callback_query(F.data == "denial_claim")
async def DenialInline(callback: CallbackQuery):
    if not await is_admin(callback):
        await callback.answer(OnlyAdmin, show_alert=True)
        return

    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="❌ Некорректно составлена жалоба",
                                     callback_data="incorrectly_denial_claim"))
    builder.add(InlineKeyboardButton(text="❌ Нарушитель не найден",
                                     callback_data="not_found_denial_claim"))
    builder.add(InlineKeyboardButton(text="❌ Ложная тревога",
                                     callback_data="false_denial_claim"))
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="actions_claim"))

    builder.adjust(1)

    await callback.message.edit_reply_markup(reply_markup=builder.as_markup())


@router.callback_query(F.data.contains("_denial_claim"))
async def ReasonDenialClaim(callback: CallbackQuery):
    if not await is_admin(callback):
        await callback.answer(OnlyAdmin, show_alert=True)
        return

    match = re.search(r'(\d+)', callback.message.text)
    ID = match.group(0)

    reason = ""
    emoji = "❌ Отклонена"

    if callback.data == "incorrectly_denial_claim":
        reason = "\n<b>Причина</b>: Некорректно составлена жалоба"
    elif callback.data == "not_found_denial_claim":
        reason = "\n<b>Причина</b>: Нарушитель не найден"
    elif callback.data == "false_denial_claim":
        reason = "\n<b>Причина</b>: Ложная тревога"

    answer = f"❌ Ваш <b>запрос №{ID}</b> был отменён! ❌{reason}"

    # Отправка написавшему пользователю об изменениях жалобы.
    additionally = await SelectValues("userID", "requests", "ID = (?)", [int(ID)])
    await callback.bot.send_message(additionally[0][0], answer)

    currentText = await SelectValues("htmlText", "requests", "ID = (?)", [int(ID)])
    currentText = currentText[0][0].split("[statusText]\n")

    currentText[1] = re.sub(
        r'</b>: .*',
        f'</b>: {emoji}{reason}',
        currentText[1],
        count=1
    )

    fullName = callback.from_user.full_name
    username = callback.from_user.username
    user_link = (
        f"<a href='https://t.me/{username}'>{fullName}</a>"
        if username
        else fullName
    )
    # delete <-
    date = datetime.now().strftime("%d.%m.%y")

    if "Обработал жалобу" not in currentText[1]:
        separator = "--------------------------------\n"
        currentText[1] = f"{currentText[1]}{separator}"
    currentText[1] = f"{currentText[1]}<b>[{date}] Обработал жалобу:</b> {user_link}\n"

    keyboard = InlineKeyboardBuilder()

    await UpdateValues("requests", "editable = 0, status = 'deny', htmlText = (?)", "ID = (?)",
                       [f"{currentText[0]}[statusText]\n{currentText[1]}", int(ID)])

    await callback.message.edit_text(currentText[1], reply_markup=keyboard.as_markup())


@router.callback_query(F.data == "accept_claim")
async def AcceptClaim(callback: CallbackQuery):
    if not await is_admin(callback):
        await callback.answer(OnlyAdmin, show_alert=True)
        return

    match = re.search(r'(\d+)', callback.message.text)
    ID = match.group(0)
    emoji = "✅ Успешно обработана"

    additionally = await SelectValues("userID", "requests", "ID = (?)", [int(ID)])
    answer = f"✅ Ваш <b>запрос №{ID}</b> был успешно принят и обработан! ✅"
    await callback.bot.send_message(additionally[0][0], answer)

    currentText = await SelectValues("htmlText", "requests", "ID = (?)", [int(ID)])
    currentText = currentText[0][0].split("[statusText]\n")

    currentText[1] = re.sub(
        r'</b>: .*',
        f'</b>: {emoji}',
        currentText[1],
        count=1
    )
    # delete ->
    fullName = callback.from_user.full_name
    username = callback.from_user.username
    user_link = (
        f"<a href='https://t.me/{username}'>{fullName}</a>"
        if username
        else fullName
    )
    # delete <-
    date = datetime.now().strftime("%d.%m.%y")

    if "Обработал жалобу" not in currentText[1]:
        separator = "--------------------------------\n"
        currentText[1] = f"{currentText[1]}{separator}"
    currentText[1] = f"{currentText[1]}<b>[{date}] Обработал жалобу:</b> {user_link}\n"

    keyboard = InlineKeyboardBuilder()

    await UpdateValues("requests", "editable = 0, status = 'accept', htmlText = (?)", "ID = (?)",
                       [f"{currentText[0]}[statusText]\n{currentText[1]}", int(ID)])

    await callback.message.edit_text(currentText[1], reply_markup=keyboard.as_markup())


@router.callback_query(F.data == "viewing_claim")
async def ViewingClaim(callback: CallbackQuery):
    if not await is_admin(callback):
        await callback.answer(OnlyAdmin, show_alert=True)
        return

    match = re.search(r'(\d+)', callback.message.text)
    ID = match.group(0)
    additionally = await SelectValues("userID, status", "requests", "ID = (?)", [int(ID)])

    emoji = "🔍 На рассмотрении"
    if additionally[0][1] != "viewing":
        answer = f"🔍 Ваш <b>запрос №{ID}</b> принят на рассмотрение администрацией! 🔍"
        await UpdateValues("requests", "status = 'viewing'", "ID = (?)", [int(ID)])
        await callback.bot.send_message(additionally[0][0], answer)

    currentText = await SelectValues("htmlText", "requests", "ID = (?)", [int(ID)])
    currentText = currentText[0][0].split("[statusText]\n")

    currentText[1] = re.sub(
        r'</b>: .*',
        f'</b>: {emoji}',
        currentText[1],
        count=1
    )
    fullName = callback.from_user.full_name
    username = callback.from_user.username
    user_link = (
        f"<a href='https://t.me/{username}'>{fullName}</a>"
        if username
        else fullName
    )
    # delete <-
    date = datetime.now().strftime("%d.%m.%y")

    if "Обработал жалобу" not in currentText[1]:
        if "была отредактирована" in currentText[1]:
            separator = "--------------------------------\n"
            currentText[1] = f"{currentText[1]}{separator}"
        currentText[1] = f"{currentText[1]}<b>[{date}] Обработал жалобу:</b> {user_link}\n"

    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(
        text="⚙ Действия",
        callback_data="actions_claim"
    ))

    await UpdateValues("requests", "editable = 0, htmlText = (?)", "ID = (?)",
                       [f"{currentText[0]}[statusText]\n{currentText[1]}", int(ID)])

    await callback.message.edit_text(currentText[1], reply_markup=keyboard.as_markup())


async def is_admin(callback: CallbackQuery):
    member = await callback.bot.get_chat_member(callback.message.chat.id, callback.from_user.id)
    return member.status in ["administrator", "creator"]
