import sqlite3
from SQLite.FrequentActions import OpenDatabase


async def InsertValues(table, values):
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
