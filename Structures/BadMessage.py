import os.path
import re
from typing import List

from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Filters.PrivateChatFilter import PrivateChatFilter
from SQLite.SelectValues import SelectValues
from SQLite.UpdateValues import UpdateValues

router = Router()
router.message.filter(PrivateChatFilter())


@router.message()
async def BadMessage(message: Message):
    await message.answer("<b>Не пойму...</b> что ты вводишь?")
    await message.answer_sticker("CAACAgIAAxkBAAEHoX1mucVzt3Z7abLiXoLUUS6Rf2lxNgACEAADwDZPE-qBiinxHwLoNQQ")


@router.callback_query()
async def InlineAccept(callback: CallbackQuery):

    if not await is_admin(callback.from_user.id, callback.message.chat.id, callback.bot):
        await callback.answer("❌ Только для админов!", show_alert=True)
        return

    # Кнопка действия: открывает Принять/Отмена/"На рассмотрении"
    if callback.data == "actions":
        builder = InlineKeyboardBuilder()

        builder.add(InlineKeyboardButton(text="✅ Принять", callback_data="accept_claim"))
        builder.add(InlineKeyboardButton(text="❌ Отказ", callback_data="denial_claim"))
        builder.add(InlineKeyboardButton(text="🔍 На рассмотрении", callback_data="viewing_claim"))

        builder.adjust(2)

        await callback.message.edit_reply_markup(reply_markup=builder.as_markup())

    elif callback.data == "denial_claim":
        builder = InlineKeyboardBuilder()

        builder.add(InlineKeyboardButton(text="❌ Некорректно составлена жалоба",
                                         callback_data="incorrectly_denial_claim"))
        builder.add(InlineKeyboardButton(text="❌ Нарушитель не найден",
                                         callback_data="not_found_denial_claim"))
        builder.add(InlineKeyboardButton(text="❌ Ложная тревога",
                                         callback_data="false_denial_claim"))
        builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="cancel_claim"))

        builder.adjust(1)

        await callback.message.edit_reply_markup(reply_markup=builder.as_markup())
    elif callback.data == "cancel_claim":
        builder = InlineKeyboardBuilder()

        builder.add(InlineKeyboardButton(text="✅ Принять", callback_data="accept_claim"))
        builder.add(InlineKeyboardButton(text="❌ Отказ", callback_data="denial_claim"))
        builder.add(InlineKeyboardButton(text="🔍 На рассмотрении", callback_data="viewing_claim"))

        builder.adjust(2)

        await callback.message.edit_reply_markup(reply_markup=builder.as_markup())
    elif callback.data == "accept_claim" or callback.data == "viewing_claim" or "denial_claim" in callback.data:
        match = re.search(r'(\d+)', callback.message.text)
        ID = match.group(0)
        await UpdateValues("requests", "editable = 0", "ID = (?)", [int(ID)])
        # ДОРАБОТАТЬ!! Нужно поле с сохранённой версией text html кодом
        additionally = await SelectValues("userID, status", "requests", "ID = (?)", [int(ID)])

        keyboard = InlineKeyboardBuilder()
        reason = ""
        if callback.data == "accept_claim":
            emoji = "✅"
            await UpdateValues("requests", "status = 'accept'", "ID = (?)", [int(ID)])
            answer = f"✅ Ваш <b>запрос №{ID}</b> был обработан! ✅"
            await callback.bot.send_message(additionally[0][0], answer)
        elif "denial_claim" in callback.data:
            emoji = "❌"
            await UpdateValues("requests", "status = 'deny'", "ID = (?)", [int(ID)])
            if callback.data == "incorrectly_denial_claim":
                reason = "\nПричина: Некорректно составлена жалоба"
            elif callback.data == "not_found_denial_claim":
                reason = "\nПричина: Нарушитель не найден"
            elif callback.data == "false_denial_claim":
                reason = "\nПричина: Ложная тревога"
            answer = f"❌ Ваш <b>запрос №{ID}</b> был отменён! ❌{reason}"
            await callback.bot.send_message(additionally[0][0], answer)
        else:
            keyboard.add(InlineKeyboardButton(
                text="⚙ Действия",
                callback_data="actions"
            ))
            emoji = "🔍"

            if additionally[0][1] != "viewing":
                answer = f"🔍 Ваш <b>запрос №{ID}</b> принят на рассмотрение! 🔍{reason}"
                await UpdateValues("requests", "status = 'viewing'", "ID = (?)", [int(ID)])
                await callback.bot.send_message(additionally[0][0], answer)
        currentText = await SelectValues("htmlText", "requests", "ID = (?)", [int(ID)])
        text = re.sub(
            r':</b> .?',
            f':</b> {emoji}{reason}',
            currentText[0][0],
            count=1
        )
        await UpdateValues("requests", "htmlText = (?)", "ID = (?)", [text, int(ID)])
        await callback.message.edit_text(text, reply_markup=keyboard.as_markup())


async def is_admin(userID: int, chatID: int, bot: Bot):
    member = await bot.get_chat_member(chatID, userID)
    return member.status in ["administrator", "creator"]



