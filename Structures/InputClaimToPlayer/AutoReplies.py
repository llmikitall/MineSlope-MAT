RequestBeenProcessed = ("<b>[Невозможно изменить жалобу]</b>:\n"
                        "Жалоба уже была обработана администратором!")

RequestCreating = "<b>[Ваша жалоба была успешно составлена]</b>\nПожалуйста, ожидайте обратной связи."


EnterFollowing = "<b>[Укажите, пожалуйста, следующее]</b>:"
EnterNick = "\n- <b>Ваш ник</b>;"
EnterIntruder = "\n- <b>Ник нарушителя</b>;"
EnterType = "\n- <b>Тип нарушения</b>;"

TextEdited = "<b>[Текст жалобы был успешно отредактирован]</b>"
PhotoEdited = "<b>[Фото жалобы было успешно отредактировано]</b>"


def EnterFollowingBoxs(boxs: list):
    text = ""
    if boxs[0][0] == "-":
        text += EnterNick
    if boxs[0][1] == "-":
        text += EnterIntruder
    if boxs[0][2] == "-":
        text += EnterType
    return EnterFollowing + text if text != "" else ""
