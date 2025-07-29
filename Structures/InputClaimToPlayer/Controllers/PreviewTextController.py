from aiogram.types import Message

from SQLite.SelectValues import SelectValues


async def PreviewText(message: Message, ID, boxs):
    additionally = await SelectValues("editable, htmlText",
                                      "requests",
                                      "ID = (?)",
                                      [int(ID[0][0])])
    if additionally[0][0] == 1:
        separator = "--------------------------------\n"

        # Составление обязательной структуры жалобы
        text = (f"<b>Жалоба №{abs(int(ID[0][0])):03d}:</b> ⚙\n"
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
