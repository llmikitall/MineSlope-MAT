import sqlite3
from SQLite.FrequentActions import OpenDatabase


# FindExitsRow - Метод, для поиска существующего значения.
# Пример: table = users, title = userID, value = 123;
# Есть ли в таблице users строка, где userID = 123? В ответе получаем либо 0, либо 1
async def FindExitsRow(table, title, value):
    with OpenDatabase() as conn:
        cur = conn.cursor()
        cur.execute(" SELECT " + title + " FROM " + table + " WHERE " + title + " =?;", [value])
        conn.commit()
        request = len(cur.fetchall())   # Можно переделать в true/false... В будущем
    return request


# FindAnyRowUsers - Метод для поиска любого столбца в таблице users:
# Пример: userID = 123, title = status -> Какой статус у пользователя userID?
def FindAnyRowUsers(userID, title):
    with OpenDatabase() as conn:
        cur = conn.cursor()
        cur.execute(" SELECT " + title + " FROM users WHERE userID =?;", [str(userID)])
        conn.commit()
        request = cur.fetchall()[0][0]
    return request


# FindMaxRequest - Метод для вычисления самого большого ID request пользователя.
# Необходим для "Создать новый запрос", при создании запроса ему присваивается максимальный номер
def FindMaxRequest(userID):
    with OpenDatabase() as conn:
        cur = conn.cursor()
        cur.execute("SELECT MAX(ID) FROM requests WHERE userID =?;", [str(userID)])
        conn.commit()
        request = cur.fetchall()[0][0]
    return request


# SelectBoxsRequest - метод, который необходим для получения всех данных из box*
def SelectBoxsRequest(ID):
    with OpenDatabase() as conn:
        cur = conn.cursor()
        cur.execute("SELECT box1, box2, box3, box4, box5, box6 FROM requests WHERE ID =?;", [int(ID)])
        conn.commit()
        request = cur.fetchall()[0]
    return request


def SelectRequestsUser(userID):
    with OpenDatabase() as conn:
        cur = conn.cursor()
        cur.execute("SELECT ID FROM requests WHERE userID =?;", [str(userID)])
        conn.commit()
        request = cur.fetchall()
    return request
