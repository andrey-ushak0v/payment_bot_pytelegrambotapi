import sqlite3


def get_my_cards(tg_id) -> list:
    try:
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM card WHERE user_id = {tg_id};")
        records = cursor.fetchall()
        return records
    except sqlite3.Error as error:
        return ("Ошибка при работе с SQLite", error)
    finally:
        if conn:
            conn.close()
