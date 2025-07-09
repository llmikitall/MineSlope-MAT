import sqlite3
from SQLite.FrequentActions import OpenDatabase


async def FindExitsRow(table, title, value):
    with OpenDatabase() as conn:
        cur = conn.cursor()
        cur.execute(" SELECT " + title + " FROM " + table + " WHERE " + title + " =?;", value)
        conn.commit()
        request = len(cur.fetchall())
    return request


def FindAnyRowUsers(userID, title):
    with OpenDatabase() as conn:
        cur = conn.cursor()
        cur.execute(" SELECT " + title + " FROM users WHERE userID =?;", [str(userID)])
        conn.commit()
        request = cur.fetchall()[0][0]
    return request


def FindMaxRequest(userID):
    with OpenDatabase() as conn:
        cur = conn.cursor()
        cur.execute("SELECT MAX(ID) FROM requests WHERE userID =?;", [str(userID)])
        conn.commit()
        request = cur.fetchall()[0][0]
    return request


def SelectBoxsRequest(ID):
    with OpenDatabase() as conn:
        cur = conn.cursor()
        cur.execute("SELECT box1, box2, box3, box4, box5 FROM requests WHERE ID =?;", [int(ID)])
        conn.commit()
        request = cur.fetchall()[0]
    return request
