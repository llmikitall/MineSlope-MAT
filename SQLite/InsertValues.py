import sqlite3
from SQLite.CreateTables import PATH_TO_DB


async def InsertValues(table, values):
    if table is "requests":
        values1 = " (userID, topicID, box1, box2, box3, box4, box5)"
        values2 = "(?, ?, ?, ?, ?, ?, ?);"
    else:
        return False
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    cur.execute(" INSERT INTO " + table + values1 + " VALUES " + values2, values)
    con.commit()
    con.close()
    return True
