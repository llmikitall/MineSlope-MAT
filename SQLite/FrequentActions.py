import os
import sqlite3


def ExitsTable(name):
    os.makedirs("Files", exist_ok=True)
    with OpenDatabase() as conn:
        cur = conn.cursor()
        cur.execute(" SELECT name FROM sqlite_master WHERE type='table' AND name=?;", ([name]))
        conn.commit()
        request = len(cur.fetchall())
    return request


def OpenDatabase():
    conn = sqlite3.connect("Files/database.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

