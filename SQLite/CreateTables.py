import sqlite3
from SQLite.FrequentActions import OpenDatabase


async def CreateTableRequests():
    with OpenDatabase() as conn:
        cur = conn.cursor()
        cur.execute(""" CREATE TABLE requests(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            userID TEXT,
                            topicID TEXT,
                            status TEXT DEFAULT 'creating',
                            box1 TEXT DEFAULT '-',
                            box2 TEXT DEFAULT '-',
                            box3 TEXT DEFAULT '-',
                            box4 TEXT DEFAULT '-',
                            box5 TEXT DEFAULT '-',
                            box6 TEXT DEFAULT '-',
                            htmlText TEXT DEFAULT '-',
                            FOREIGN KEY (userID)
                                REFERENCES users(userID)
                                ON DELETE CASCADE
                                ON UPDATE CASCADE);
        """)
        conn.commit()


async def CreateTableUsers():
    with OpenDatabase() as conn:
        cur = conn.cursor()
        cur.execute(""" CREATE TABLE users(
                            userID TEXT PRIMARY KEY,
                            status INTEGER DEFAULT 0,
                            request TEXT DEFAULT '-',
                            oMainMenu INTEGER DEFAULT 0,
                            oSendMessageMenu INTEGER DEFAULT 0);
        """)
        conn.commit()
