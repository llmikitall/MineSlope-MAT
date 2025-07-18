import os.path
import re

from aiogram import Router, F, Bot
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Filters.PrivateChatFilter import PrivateChatFilter
from SQLite.SelectValues import SelectValues
from SQLite.UpdateValues import UpdateValues

router = Router()
router.message.filter(PrivateChatFilter())


@router.message(F.photo)
async def BadPhoto(message: Message):
    DOWNLOAD_FOLDER = "Files"
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    file_path = file.file_path

    file_name = f"file_{message.from_user.id}.jpg"
    save_path = os.path.join(DOWNLOAD_FOLDER, file_name)
    await message.bot.download_file(file_path, save_path)


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

        # ДОРАБОТАТЬ!! Нужно поле с сохранённой версией text html кодом
        listing = await SelectValues("*", "requests", "ID = (?)", [int(match.group(0))])

        keyboard = InlineKeyboardBuilder()
        reason = ""
        if callback.data == "accept_claim":
            emoji = "✅"
            await UpdateValues("requests", "status = 'accept'", "ID = (?)", [int(match.group(0))])
            answer = f"✅ Ваш <b>запрос №{listing[0][0]}</b> был обработан! ✅"
            await callback.bot.send_message(listing[0][1], answer)
        elif "denial_claim" in callback.data:
            emoji = "❌"
            await UpdateValues("requests", "status = 'deny'", "ID = (?)", [int(match.group(0))])
            if callback.data == "incorrectly_denial_claim":
                reason = "Причина: Некорректно составлена жалоба"
            elif callback.data == "not_found_denial_claim":
                reason = "Причина: Нарушитель не найден"
            elif callback.data == "false_denial_claim":
                reason = "Причина: Ложная тревога"
            answer = f"❌ Ваш <b>запрос №{listing[0][0]}</b> был отменён! ❌\n{reason}"
            await callback.bot.send_message(listing[0][1], answer)
        else:
            keyboard.add(InlineKeyboardButton(
                text="⚙ Действия",
                callback_data="actions"
            ))
            emoji = "🔍"

            if listing[0][3] != "viewing":
                answer = f"🔍 Ваш <b>запрос №{listing[0][0]}</b> принят на рассмотрение! 🔍\n{reason}"
                await UpdateValues("requests", "status = 'viewing'", "ID = (?)", [int(match.group(0))])
                await callback.bot.send_message(listing[0][1], answer)
        currentText = listing[0][10]
        text = re.sub(
            r':</b> .?',
            f':</b> {emoji}\n{reason}',
            currentText,
            count=1
        )
        await callback.message.edit_text(text, reply_markup=keyboard.as_markup())


async def is_admin(userID: int, chatID: int, bot: Bot):
    member = await bot.get_chat_member(chatID, userID)
    return member.status in ["administrator", "creator"]



