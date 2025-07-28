from SQLite.FrequentActions import OpenDatabase


async def insert_values(table, values):
    if table == "requests":
        values1 = " (userID, topicID, box1, box2, box3, box4, box5, box6)"
        values2 = "(?, ?, ?, ?, ?, ?, ?, ?);"
    elif table == "users":
        values1 = " (userID)"
        values2 = "(?);"
    else:
        return False
    with OpenDatabase() as conn:
        cur = conn.cursor()
        cur.execute(" INSERT INTO " + table + values1 + " VALUES " + values2, values)
        conn.commit()
    return True


# InsertValues - Метод, для обращения к базе данных
async def InsertValues(table, titles, parameters, values):
    # Открываем базу данных, это уже готовый метод, потому ничего передавать не надо:
    with OpenDatabase() as conn:
        # Создаём cur и присваеваем ему курсор базы данных (Курсор позволяет...
        # ...обращаться к базе данных с помощью запросов).
        cur = conn.cursor()
        # Здесь случается запрос к базе данных. Большущими буквами пишутся ключевые слова:
        # INSERT, UPDATE, SELECT. Вот примерно так надо сделать... Правда тут нужно знание SQL языка.
        cur.execute("INSERT INTO " + table + titles + " VALUES " + parameters, values)
        # Сохранение базы данных.
        conn.commit()
    return True
