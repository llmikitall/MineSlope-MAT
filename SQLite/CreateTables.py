import sqlite3


PATH_TO_DB = "Files/database.db"


async def CreateTableRequest():
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    cur.execute(""" CREATE TABLE requests IF NOT EXITS(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        userID TEXT,
                        topicID TEXT,
                        status TEXT DEFAULT 'await',
                        box1 TEXT,
                        box2 TEXT,
                        box3 TEXT,
                        box4 TEXT,
                        box5 TEXT);
    """)
    con.commit()
    con.close()

