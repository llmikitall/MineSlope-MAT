import sqlite3
from SQLite.FrequentActions import OpenDatabase


def UpdateValue(userID, table, title, value):
    with OpenDatabase() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE " + table + " SET " + title + " = (?) WHERE userID = (?);",
                    [f"{value}", f"{userID}"])
        conn.commit()


async def UpdateValues(table, titles, where, values):
    with OpenDatabase() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE " + table + " SET " + titles + " WHERE " + where, values)
        conn.commit()


def UpdateBoxValue(userID, title, value):
    with OpenDatabase() as conn:
        cur = conn.cursor()
        cur.execute("SELECT request FROM users WHERE userID = (?);", [str(userID)])
        ID = cur.fetchall()[0][0]
        cur.execute("UPDATE requests SET " + title + " = (?) WHERE ID = (?);", [value, int(ID)])
        conn.commit()
