import sqlite3
from SQLite.FrequentActions import OpenDatabase


async def DropTable(table):
    with OpenDatabase() as conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE " + table + ";")
        conn.commit()
