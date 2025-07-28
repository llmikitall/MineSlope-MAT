from SQLite.FrequentActions import OpenDatabase


async def DeleteValues(table, where, values):
    with OpenDatabase() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM " + table + " WHERE " + where, values)
        conn.commit()
    return True
